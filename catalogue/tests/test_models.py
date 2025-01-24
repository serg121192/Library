from django.contrib.auth import get_user_model
from django.test import TestCase

from catalogue.models import LiteraryFormat, Author, Book


class ModelsTests(TestCase):
    def test_literary_format_str(self):
        literary_format = LiteraryFormat.objects.create(name="test_format")
        self.assertEqual(str(literary_format), literary_format.name)

    def test_author_str(self):
        author = get_user_model().objects.create(
            username="test_author",
            password="Test123!",
            first_name="first_name",
            last_name="last_name",
        )
        self.assertEqual(
            str(author),
            f"{author.username} ({author.first_name} {author.last_name})"
        )

    def test_book_str(self):
        literary_format = LiteraryFormat.objects.create(name="test_format")
        book = Book.objects.create(
            title="Test Book",
            price=10.50,
            format=literary_format,
        )
        self.assertEqual(
            str(book),
            f"{book.title} (price: {book.price}, format: {book.format})"
        )

    def test_author_with_pseudonym(self):
        username = "test_author"
        password = "Test123!"
        pseudonym = "test_pseudonym"
        author = get_user_model().objects.create_user(
            username=username,
            password=password,
            pseudonym=pseudonym,
        )
        self.assertEqual(author.username, username)
        self.assertTrue(author.password, password)
        self.assertEqual(author.pseudonym, pseudonym)
