from django.conf import settings
from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())

from django.forms import ModelForm
from django import forms
from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User
from django.contrib.auth.forms import (AdminPasswordChangeForm, UserChangeForm, UserCreationForm)

from .models import User, Privilege, SessionToken
from common import models as common_models

from rest_framework.authtoken.admin import TokenAdmin

# registering token fields into admin
TokenAdmin.raw_id_fields = ('user',)


# move to forms.py?
class SessionTokenChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.key


# move to forms.py?
class SessionTokenInlineAdminForm(ModelForm):
    # this means no tokens will be shown when creating new SessionTokens from the page. and that's okay.
    token = SessionTokenChoiceField(queryset=SessionToken.objects.filter(user=None))

    class Meta:
        model = SessionToken
        fields = []

    def __init__(self, *args, **kwargs):
        super(SessionTokenInlineAdminForm, self).__init__(*args, **kwargs)
        # self.initial['key'] = SessionToken.generate_key()


class AddressInline(admin.StackedInline):
    model = common_models.Address
    extra = 0


# TODO: [P3] Need to make session creation more foolproof
class SessionTokenInline(admin.StackedInline):
    form = SessionTokenInlineAdminForm
    model = SessionToken
    extra = 0



    # def clean_email(self):
    #     email = self.cleaned_data['username']
    #     return email

#
# class UserAdmin(UserAdmin):
#     model = User
#     form = UserForm
#
#     inlines = [SessionTokenInline, AddressInline, ]
#     list_display = ('email', 'first_name', 'last_name', 'is_staff')
#     list_filter = ('is_staff',)
#     search_fields = ('email',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # custom:
    form = UserChangeForm

    # referenced:
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (

        (None, {'fields': ['email', 'password', 'is_registered', ]}),
        ('Business information', {'fields': ['privilege', 'company', ]}),
        ('Personal information', {'fields': ['first_name', 'last_name', 'phone', ]}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'date_registered',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    inlines = [SessionTokenInline, AddressInline, ]
    list_display = ('id', 'email', 'is_registered', 'privilege', )
    list_filter = ('date_joined', 'is_staff', 'is_superuser', 'is_active', )
    search_fields = ('email', 'first_name', 'last_name', )
    ordering = ('date_joined',)
    # filter_horizontal = ('groups', 'user_permissions',)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(UserAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super(UserAdmin, self).get_form(request, obj, **defaults)

    def get_urls(self):
        return [
            url(
                r'^(.+)/password/$',
                self.admin_site.admin_view(self.user_change_password),
                name='auth_user_password_change',
            ),
        ] + super(UserAdmin, self).get_urls()

    def lookup_allowed(self, lookup, value):
        # See #20078: we don't want to allow any lookups involving passwords.
        if lookup.startswith('password'):
            return False
        return super(UserAdmin, self).lookup_allowed(lookup, value)

    @sensitive_post_parameters_m
    @csrf_protect_m
    @transaction.atomic
    def add_view(self, request, form_url='', extra_context=None):
        # It's an error for a user to have add permission but NOT change
        # permission for users. If we allowed such users to add users, they
        # could create superusers, which would mean they would essentially have
        # the permission to change users. To avoid the problem entirely, we
        # disallow users from adding users if they don't have change
        # permission.
        if not self.has_change_permission(request):
            if self.has_add_permission(request) and settings.DEBUG:
                # Raise Http404 in debug mode so that the user gets a helpful
                # error message.
                raise Http404(
                    'Your user does not have the "Change user" permission. In '
                    'order to add users, Django requires that your user '
                    'account have both the "Add user" and "Change user" '
                    'permissions set.')
            raise PermissionDenied
        if extra_context is None:
            extra_context = {}
        username_field = self.model._meta.get_field(self.model.USERNAME_FIELD)
        defaults = {
            'auto_populated_fields': (),
            'username_help_text': username_field.help_text,
        }
        extra_context.update(defaults)
        return super(UserAdmin, self).add_view(request, form_url,
                                               extra_context)

    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=''):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = self.get_object(request, unquote(id))
        if user is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                'name': force_text(self.model._meta.verbose_name),
                'key': escape(id),
            })
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(request, form, None)
                self.log_change(request, user, change_message)
                msg = ugettext('Password changed successfully.')
                messages.success(request, msg)
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect(
                    reverse(
                        '%s:%s_%s_change' % (
                            self.admin_site.name,
                            user._meta.app_label,
                            user._meta.model_name,
                        ),
                        args=(user.pk,),
                    )
                )
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _('Change password: %s') % escape(user.get_email()),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': (IS_POPUP_VAR in request.POST or
                         IS_POPUP_VAR in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
        }
        context.update(self.admin_site.each_context(request))

        request.current_app = self.admin_site.name

        return TemplateResponse(request,
            self.change_user_password_template or
            'admin/auth/user/change_password.html',
            context)

# OLD CLASS
# class UserAdmin(admin.ModelAdmin):
#     form = UserForm
#     # No point adding password field -- meaningless?
#     fieldsets = [
#         (None, {'fields': ['email', 'username', 'is_registered', 'date_registered', ]}),
#         ('Business information', {'fields': ['privilege', 'company', ]}),
#         ('Personal information', {'fields': ['first_name', 'last_name', 'phone', ]}),
#         ('Account information', {'fields': ['password', 'last_login', 'date_joined', 'is_active', 'is_staff', ]}),
#     ]
#     inlines = [SessionTokenInline, AddressInline, ]
#     list_display = ('id', 'email', 'username', 'is_registered', 'privilege', )
#     list_filter = ['date_joined']
#     search_fields = ['email']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class PrivilegeAdmin(admin.ModelAdmin):
    # No point adding password field -- meaningless?
    fieldsets = [
        (None, {'fields': ['name', ]}),
        ('Personal', {'fields': ['user_read',
                                 'user_write',
                                 'user_verify',
                                 'user_delete', ]}),
        ('Business: Transaction Access', {'fields': ['company_read_transactions',
                                                     'company_write_transactions',
                                                     'company_verify_transactions',
                                                     'company_delete_transactions', ]}),
        ('Business: Document Access', {'fields': ['company_read_documents',
                                                  'company_write_documents',
                                                  'company_verify_documents',
                                                  'company_delete_documents', ]}),
        ('Admin', {'fields': ['all_read',
                              'all_verify',
                              'all_write',
                              'all_delete', ]}),
    ]
    list_display = ('name',
                    'user_read',
                    'user_write',
                    'company_read_transactions',
                    'company_write_transactions',
                    'company_read_documents',
                    'company_write_documents',
                    'all_read',
                    'all_write',
                    )

admin.site.register(Privilege, PrivilegeAdmin)


class SessionTokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'privilege', 'created', )
    list_filter = ['created']
    search_fields = ['user']

admin.site.register(SessionToken, SessionTokenAdmin)
