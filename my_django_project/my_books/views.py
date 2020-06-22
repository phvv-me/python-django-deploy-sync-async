from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy

from .models import Book


class BookList(ListView):
    model = Book
    context_object_name = "books"


class BookCreate(CreateView):
    model = Book
    extra_context = {"is_create": True}
    success_url = reverse_lazy("book-list")
    fields = "__all__"


class BookRead(DetailView):
    model = Book
    context_object_name = "book"


class BookUpdate(UpdateView):
    model = Book
    context_object_name = "book"
    success_url = reverse_lazy("book-list")
    fields = ("pages", "language")


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy("book-list")
