from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class TestAdminPage(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.author = get_user_model().objects.create_user(
            username="author",
            password="testauthor",
            pseudonym="test_pseudo",
        )

    def test_author_pseudo_listed(self):
        """
        Test that the author pseudo is listed on the admin page.
        :return:
        """
        url = reverse("admin:catalogue_author_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.author.pseudonym)