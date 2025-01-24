from django.contrib.auth import get_user_model
from django.test import TestCase

from catalogue.forms import AuthorCreationForm


class AuthorCreationFormTest(TestCase):
    def test_new_author_creation_with_valid_data(self):
        form_data = {
            "username": "test_user",
            "password1": "Test123!",
            "password2": "Test123!",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "pseudonym": "Test_pseudo"
        }
        form = AuthorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)