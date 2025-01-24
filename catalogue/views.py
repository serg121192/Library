from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from catalogue.forms import AuthorCreationForm, BookCreateUpdateForm, BookSearchForm
from catalogue.models import Book, Author, LiteraryFormat


def index(request: HttpRequest) -> HttpResponse:
    num_books = Book.objects.count()
    num_authors = Author.objects.count()
    literary_formats = LiteraryFormat.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_authors": num_authors,
        "literary_formats_list": literary_formats,
        "num_visits": request.session["num_visits"],
    }

    return render(
        request,
        "catalogue/index.html",
        context=context,
    )


class LiteraryFormatsListView(LoginRequiredMixin, generic.ListView):
    model = LiteraryFormat
    template_name = "catalogue/literary_formats_list.html"
    context_object_name = "literary_formats_list"


class BooksListView(LoginRequiredMixin, generic.ListView):
    model = Book
    template_name = "catalogue/books_list.html"
    context_object_name = "books_list"
    paginate_by = 2

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super(BooksListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title")
        context["search_form"] = BookSearchForm(
            initial={
                "title": title
            },
        )
        return context

    def get_queryset(self):
        queryset = Book.objects.select_related("format")
        form = BookSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                title__icontains=form.cleaned_data["title"]
            )
        return queryset


class AuthorsListView(LoginRequiredMixin, generic.ListView):
    model = Author
    template_name = "catalogue/authors_list.html"
    context_object_name = "authors_list"


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = "catalogue/book_details.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context["book_authors"] = book.authors.values_list("username", flat=True)
        return context


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    form_class = BookCreateUpdateForm
    template_name = "catalogue/book_form.html"
    success_url = reverse_lazy("catalogue:books-list")


class BookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Book
    form_class = BookCreateUpdateForm


class BookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Book
    template_name = "catalogue/book_delete_confirmation.html"
    success_url = reverse_lazy("catalogue:books-list")


class AuthorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Author
    form_class = AuthorCreationForm
    success_url = reverse_lazy("catalogue:authors-list")
    template_name = "catalogue/author_create.html"


class LiteraryFormatCreateView(LoginRequiredMixin, generic.CreateView):
    model = LiteraryFormat
    fields = "__all__"
    success_url = reverse_lazy("catalogue:literary-formats-list")
    template_name = "catalogue/literary_format_form.html"


class LiteraryFormatUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = LiteraryFormat
    fields = "__all__"
    success_url = reverse_lazy("catalogue:literary-formats-list")
    template_name = "catalogue/literary_format_form.html"


class LiteraryFormatDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = LiteraryFormat
    template_name = "catalogue/literary_format_delete_confirmation.html"
