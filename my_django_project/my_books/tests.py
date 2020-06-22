import pytest

from django.test import Client
from django.urls import reverse
from django.forms.models import model_to_dict

from rest_framework.status import *
from rest_framework.test import APIClient

from .models import Book
from django.urls import get_resolver

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
        url = reverse("book-list")
        response = client.get(url)

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
            Book.objects.get(pk=1)  # deleted book
            assert excinfo.value == "Book matching query does not exist"

    def test_unavailable_language_failure(self):
        """Ensure we can create a new book."""

        client = Client()

        body = {
            "title": "Moby Dick",
            "author": "Herman Melville",
            "language": "FR",
            "pages": 821,
        }

        # create book
        url = reverse("book-create")
        response = client.post(url, body, follow=True)
        language_errors = list(response.context_data["form"].errors["language"])

        # even though it fails to create, the error is displayed as a form error
        # meaning the response has a 2XX status
        assert response.status_code is HTTP_200_OK
        assert language_errors == [
            "Select a valid choice. FR is not one of the available choices."
        ]


@pytest.mark.django_db
class TestBooksREST:
    def test_create(self):
        """Ensure we can create a new book: POST /books/"""
        client = APIClient()

        body = {
            "title": "Moby Dick",
            "author": "Herman Melville",
            "language": "EN",
            "pages": 698,
        }

        # create book
        url = reverse("book-rest-list")
        response = client.post(url, body)

        assert response.status_code is HTTP_201_CREATED

        # read the created book
        new_book = Book.objects.get(pk=1)

        assert model_to_dict(new_book) == {"id": 1, **body}

    def test_read_one(self, books):
        """Ensure we can retrieve one book: GET /books/1"""
        client = APIClient()

        url = reverse("book-rest-detail", kwargs={"pk": 1})
        response = client.get(url)

        body = {
            "id": 1,
            "title": "Moby Dick",
            "author": "Herman Melville",
            "language": "english",
            "pages": 677,
        }

        assert response.status_code is HTTP_200_OK
        assert response.json() == body

    def test_read_all(self, books):
        """Ensure we can list all books: GET /books/"""
        client = APIClient()

        url = reverse("book-rest-list")
        response = client.get(url)

        body = [
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

        assert response.status_code is HTTP_200_OK
        assert response.json() == body

    def test_update(self, books):
        """Ensure we can update a book: PUT /books/1"""
        client = APIClient()

        body = {
            "title": "Moby Dick",
            "author": "Herman Melville",
            "language": "JP",
            "pages": 455,
        }

        url = reverse("book-rest-detail", kwargs={"pk": 1})
        response = client.put(url, body)

        assert response.status_code is HTTP_200_OK

        # assert the book was updated
        updated_book = Book.objects.first()

        assert model_to_dict(updated_book) == {"id": 1, **body}

    def test_partial_update(self, books):
        """Ensure we can partial update a book: PATCH /books/1"""
        client = APIClient()

        body = {
            "language": "JP",
        }

        url = reverse("book-rest-detail", kwargs={"pk": 1})
        response = client.patch(url, body)

        assert response.status_code is HTTP_200_OK

        # assert the book was updated
        updated_book = Book.objects.first()

        assert updated_book.language == body["language"]

    def test_delete(self, books):
        """Ensure we can delete a book: DELETE /books/1"""
        client = APIClient()

        url = reverse("book-rest-detail", kwargs={"pk": 1})
        response = client.delete(url)

        assert response.status_code is HTTP_204_NO_CONTENT

        # reading the book should fail
        with pytest.raises(Book.DoesNotExist) as excinfo:
            Book.objects.get(pk=1)  # deleted book
            assert excinfo.value == "Book matching query does not exist"


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
