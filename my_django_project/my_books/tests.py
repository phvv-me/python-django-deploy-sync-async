from django.test import Client
from django.urls import reverse
from django.forms.models import model_to_dict

import pytest
from rest_framework.status import *
from .models import Book

# fixtures


@pytest.fixture
def books():
    return Book.objects.bulk_create(
        [
            Book(
                title="Moby Dick",
                author="Herman Melville",
                language="english",
                pages=677,
            ),
            Book(
                title="As Crônicas de Nárnia",
                author="C. S. Lewis",
                language="portuguese",
                pages=752,
            ),
            Book(
                title="Harry Potter und Der Stein der Weisen",
                author="J. K. Rowling",
                language="german",
                pages=337,
            ),
            Book(
                title="羊をめぐる冒険",
                author="Haruki Murakami",
                language="japanese",
                pages=331,
            ),
        ]
    )


@pytest.mark.django_db
class TestBooksServerSide:
    def test_create(self):
        """Ensure we can create a new book."""

        client = Client()

        body = {
            "title": "Moby Dick",
            "author": "Herman Melville",
            "language": "EN",
            "pages": 698,
        }

        # create book
        url = reverse("book-create")
        response = client.post(url, body, follow=True)

        assert response.status_code is HTTP_200_OK
        # assert response.redirect_chain == [("/books/", 302)]

        # read the created book
        new_book = Book.objects.get(pk=1)

        assert model_to_dict(new_book) == {"id": 1, **body}

    def test_read_one(self, books):
        """Ensure we can read the book data."""
        client = Client()

        book = {
            "id": 1,
            "title": "Moby Dick",
            "author": "Herman Melville",
            "language": "english",
            "pages": 677,
        }

        url = reverse("book-read", kwargs={"pk": 1})
        response = client.get(url)

        assert response.status_code is HTTP_200_OK
        assert book == model_to_dict(response.context["book"])

    def test_read_all(self, books):
        """Ensure we can see a list of all the books."""
        client = Client()

        context = [
            {
                "id": 1,
                "title": "Moby Dick",
                "author": "Herman Melville",
                "language": "english",
                "pages": 677,
            },
            {
                "id": 2,
                "title": "As Crônicas de Nárnia",
                "author": "C. S. Lewis",
                "language": "portuguese",
                "pages": 752,
            },
            {
                "id": 3,
                "title": "Harry Potter und Der Stein der Weisen",
                "author": "J. K. Rowling",
                "language": "german",
                "pages": 337,
            },
            {
                "id": 4,
                "title": "羊をめぐる冒険",
                "author": "Haruki Murakami",
                "language": "japanese",
                "pages": 331,
            },
        ]

        response = client.get("/books/")

        assert response.status_code is HTTP_200_OK
        assert context == list(response.context["books"].values())

    def test_update(self, books):
        """Ensure we can update a book."""
        client = Client()

        body = {
            "title": "Moby Dick",
            "author": "Herman Melville",
            "language": "JP",
            "pages": 455,
        }

        url = reverse("book-update", kwargs={"pk": 1})
        response = client.post(url, body, follow=True)  # forms cannot recieve "PUT"

        assert response.status_code is HTTP_200_OK
        assert response.redirect_chain == [("/books/", 302)]

        # assert the book was updated
        updated_book = Book.objects.first()

        assert model_to_dict(updated_book) == {"id": 1, **body}

    def test_delete(self, books):
        """Ensure we can delete a book."""
        client = Client()

        url = reverse("book-delete", kwargs={"pk": 1})
        response = client.delete(url, follow=True)

        assert response.status_code is HTTP_200_OK
        assert response.redirect_chain == [("/books/", 302)]

        # reading the book should fail
        with pytest.raises(Book.DoesNotExist) as excinfo:
            deleted_book = Book.objects.get(pk=1)
            assert excinfo.value is "Book matching query does not exist"


@pytest.mark.django_db
class TestBooksREST:
    def test_identify_options(self):
        """Ensure the allowed methods are OPTIONS, GET, HEAD, POST, PUT, PATCH, DELETE"""
        assert False

    def test_create(self):
        """Ensure we can create a new book: POST /books/"""
        assert False

    def test_read_one(self, books):
        """Ensure we can retrieve one book: GET /books/1"""
        assert False

    def test_read_all(self, books):
        """Ensure we can list all books: GET /books/"""
        assert False

    def test_update(self, books):
        """Ensure we can update a book: PUT /books/1"""
        assert False

    def test_partial_update(self, books):
        """Ensure we can partial update a book: PATCH /books/1"""
        assert False

    def test_delete(self, books):
        """Ensure we can delete a book: DELETE /books/1"""
        assert False


@pytest.mark.django_db
class TestBooksGraphQL:
    def test_identify_options(self):
        """Ensure the allowed methods are OPTIONS, GET, HEAD, POST, PUT, PATCH, DELETE"""
        assert False

    def test_create(self):
        """Ensure we can create a new book: POST /books/"""
        assert False

    def test_read_one(self, books):
        """Ensure we can retrieve one book: GET /books/1"""

        assert False

    def test_read_all(self, books):
        """Ensure we can list all books: GET /books/"""
        assert False

    def test_update(self, books):
        """Ensure we can update a book: PUT /books/1"""
        assert False

    def test_partial_update(self, books):
        """Ensure we can partial update a book: PATCH /books/1"""
        assert False

    def test_delete(self, books):
        """Ensure we can delete a book: DELETE /books/1"""
        assert False
