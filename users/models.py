from __future__ import unicode_literals

import datetime
import binascii
import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.contenttypes.models import ContentType
from django.core import validators
from django.core.mail import send_mail

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from companies import models as company_models


class Privilege(models.Model):
    name = models.CharField(max_length=30)

    # Admin
    all_write = models.BooleanField(default=False, )
    all_delete = models.BooleanField(default=False, )
    all_read = models.BooleanField(default=False, )
    all_verify = models.BooleanField(default=False, )

    # Business:
    company_read_transactions = models.BooleanField(default=False, )
    company_write_transactions = models.BooleanField(default=False, )
    company_verify_transactions = models.BooleanField(default=False, )
    company_delete_transactions = models.BooleanField(default=False, )

    company_read_documents = models.BooleanField(default=False, )
    company_write_documents = models.BooleanField(default=False, )
    company_verify_documents = models.BooleanField(default=False, )
    company_delete_documents = models.BooleanField(default=False, )

    # User's data:
    user_read = models.BooleanField(default=False, )
    user_write = models.BooleanField(default=False, )
    user_verify = models.BooleanField(default=False, )
    user_delete = models.BooleanField(default=False, )

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{} '{}': name='{}'>".format(
            self.__class__.__name__,
            self.id, self.name)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(
        _('email address'),
        max_length=30,
        unique=True,
        help_text=_('Required. This is used as your username.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid email. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)






@python_2_unicode_compatible
class User(AbstractUser):
    # Email, username, first_name, last_name, password, last_login, date_joined, is_active, is_staff
    # already handled by Abstract user

    # note: registering (by user) is different from joining (auto-created by system)
    is_registered = models.BooleanField(default=False,)
    date_registered = models.DateTimeField(_('date registered'), default=timezone.now)

    # optional field; for future use. Not storing these information for now
    phone = models.CharField(max_length=30, blank=True, )

    # relationship: many users have 1 privilege (This is their MAX privilege when creating new session tokens)
    privilege = models.ForeignKey(Privilege, on_delete=models.CASCADE, blank=True, null=True,
                                  default=Privilege.objects.get_or_create(name="No privilege")[0].id)

    # relationship: many users have 1 company (works for)
    company = models.ForeignKey(company_models.Company, on_delete=models.CASCADE, blank=True, null=True, )

    def __str__(self):
        return self.email

    def __repr__(self):
        return "<{} '{}': privilege='{}', registered='{}'>".format(
            self.__class__.__name__,
            self.email, self.privilege, self.is_registered)

    # example
    def was_registered_recently(self):
        return self.date_registered >= timezone.now() - datetime.timedelta(days=1)

    # def get_absolute_url(self):
    #     return reverse('users:detail', kwargs={'username': self.username})


# overrides AbstractUser defaults (not using, just using username)
# User._meta.get_field('email').blank = False
# User._meta.get_field('email')._unique = True

# http://stackoverflow.com/questions/27043349/how-to-use-custom-token-model-in-django-rest-framework
# Adapted from rest_framework.authtoken.models.Token
# need full override since User now has one to many relationship with Tokens
@python_2_unicode_compatible
class SessionToken(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='session_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    # relationship: many tokens have 1 privilege. Note: all tokens must have a privilege
    privilege = models.ForeignKey(Privilege, on_delete=models.CASCADE)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/tomchristie/django-rest-framework/issues/705
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = _("SessionToken")
        verbose_name_plural = _("SessionTokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(SessionToken, self).save(*args, **kwargs)

    # added static method -- hopefully this doesn't break anything. Also removed self from args
    @staticmethod
    def generate_key():
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

    def __repr__(self):
        return "<{}: '{}': user='{}'>".format(
            self.__class__.__name__,
            self.key, self.user)
