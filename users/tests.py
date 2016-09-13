import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import User


def create_user():
    """
    Creates a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    return User.objects.create(email="test@omnibadge.com", username="testuser", first_name="test",
                               last_name="test_last", password="testpass", )


class UserMethodTests(TestCase):

    def test_that_user_can_be_created(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """

        new_user = create_user()
        self.assertEqual(new_user.was_registered_recently(), True)
