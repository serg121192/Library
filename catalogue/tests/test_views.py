from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from catalogue.models import LiteraryFormat, Book

LITERARY_FORMATS_URL = reverse("catalogue:literary-formats-list")
BOOKS_LIST_URL = reverse("catalogue:books-list")

class PublicLiteraryFormatsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(LITERARY_FORMATS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateLiteraryFormatsTest(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(
            username="author",
            password="testAuthor"
        )
        self.client.force_login(self.author)

    def test_get_literary_formats_for_logged_in_author(self):
        new_lit_formats = ["drama", "poem", "poetry"]
        for lit_format in new_lit_formats:
            LiteraryFormat.objects.create(name=lit_format)

        response = self.client.get(LITERARY_FORMATS_URL)
        self.assertEqual(response.status_code, 200)
        literary_formats = LiteraryFormat.objects.all()
        self.assertEqual(
            list(literary_formats),
            list(response.context["literary_formats_list"]),
        )
        self.assertTemplateUsed(
            response,
            "catalogue/literary_formats_list.html"
        )


class PublicBooksListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(BOOKS_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateBooksListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="User123!"
        )
        self.client.force_login(self.user)

    def test_books_list_for_logged_in_user(self):
        new_lit_formats = ["drama", "poem", "poetry"]
        for lit_format in new_lit_formats:
            LiteraryFormat.objects.create(name=lit_format)
        formats = {
            format.name: format for format in LiteraryFormat.objects.all()
        }
        books = [
            {
                "title": "Harry Potter and the Philosopher's Stone",
                "price": 10.50,
                "format": "poem",
            },
            {
                "title": "Harry Potter and the Chamber of Secrets",
                "price": 10.59,
                "format": "poem",
            },
            {
                "title": "Romeo and Juliet",
                "price": 9.55,
                "format": "drama",
            },
            {
                "title": "Kobzar",
                "price": 19.99,
                "format": "poetry",
            }
        ]
        for book in books:
            if book["format"] in formats:
                Book.objects.create(
                    title=book["title"],
                    price=book["price"],
                    format=formats[book["format"]],
                )
        response = self.client.get(BOOKS_LIST_URL)
        self.assertEqual(response.status_code, 200)
        books_list = Book.objects.all()
        res_books = response.context["books_list"]
        for res_book in res_books:
            self.assertIn(
                res_book,
                list(books_list),
            )
        search_title = "Harry"
        filtered_books = Book.objects.filter(title__icontains=search_title)
        response = self.client.get(BOOKS_LIST_URL, {"title": search_title})
        self.assertEqual(
            list(filtered_books),
            list(response.context["books_list"]),
        )
        self.assertTemplateUsed(
            response,
            "catalogue/books_list.html"
        )
        self.assertEqual(
            response.context["search_form"].initial["title"],
            search_title,
        )


class PrivateAuthorCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="User123!"
        )
        self.client.force_login(self.user)

    def test_create_author(self):
        form_data = {
            "username": "new_author",
            "password1": "Test123!",
            "password2": "Test123!",
            "first_name": "new_author_first_name",
            "last_name": "new_author_last_name",
            "pseudonym": "new_author_pseudonym",
        }
        self.client.post(reverse("catalogue:author-create"), data=form_data)
        new_author = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_author.username, form_data["username"])
        self.assertEqual(new_author.first_name, form_data["first_name"])
        self.assertEqual(new_author.last_name, form_data["last_name"])
        self.assertEqual(new_author.pseudonym, form_data["pseudonym"])
