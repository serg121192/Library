from django.urls import path
from django.views.generic import RedirectView

from catalogue.views import (
    index,
    LiteraryFormatsListView,
    BooksListView,
    AuthorsListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    AuthorCreateView,
    LiteraryFormatCreateView,
    LiteraryFormatUpdateView,
    LiteraryFormatDeleteView, BookCreateView,
)


urlpatterns = [
    path('', index, name='index'),
    path("literary-formats/", LiteraryFormatsListView.as_view(), name="literary-formats-list"),
    path("literary-formats/create/", LiteraryFormatCreateView.as_view(), name="literary-format-create"),
    path("literary-formats/<int:pk>/update/", LiteraryFormatUpdateView.as_view(), name="literary-format-update"),
    path("literary-formats/<int:pk>/delete/", LiteraryFormatDeleteView.as_view(), name="literary-format-delete"),
    path("books/", BooksListView.as_view(), name="books-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/create/", BookCreateView.as_view(), name="book-create"),
    path("books/<int:pk>/update/", BookUpdateView.as_view(), name="book-update"),
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),
    path("authors/", AuthorsListView.as_view(), name="authors-list"),
    path("authors/create/", AuthorCreateView.as_view(), name="author-create"),
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico")),
]


app_name = "catalogue"
