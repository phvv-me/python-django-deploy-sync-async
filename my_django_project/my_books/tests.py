from collections import OrderedDict

import pytest

from django.test import Client
from django.urls import reverse
from django.forms.models import model_to_dict

from rest_framework.status import *
from rest_framework.test import APIClient

from graphene.test import Client as GrapheneClient

from .models import Book
from .schema import schema

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
    def test_create_server_side(self, benchmark):
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
        response = benchmark(client.post, url, body, follow=True)

        assert response.status_code is HTTP_200_OK
        # assert response.redirect_chain == [("/books/", 302)]

        # read the created book
        new_book = Book.objects.get(pk=1)

        assert model_to_dict(new_book) == {"id": 1, **body}

    def test_read_one_server_side(self, benchmark, books):
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
        response = benchmark(client.get, url)

        assert response.status_code is HTTP_200_OK
        assert book == model_to_dict(response.context["book"])

    def test_read_all_server_side(self, benchmark, books):
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
        response = benchmark(client.get, url)

        assert response.status_code is HTTP_200_OK
        assert context == list(response.context["books"].values())

    def test_update_server_side(self, benchmark, books):
        """Ensure we can update a book."""
        client = Client()

        body = {
            "title": "Moby Dick",
            "author": "Herman Melville",
            "language": "JP",
            "pages": 455,
        }

        url = reverse("book-update", kwargs={"pk": 1})
        response = benchmark(
            client.post, url, body, follow=True
        )  # forms cannot recieve "PUT"

        assert response.status_code is HTTP_200_OK
        assert response.redirect_chain == [("/books/", 302)]

        # assert the book was updated
        updated_book = Book.objects.first()

        assert model_to_dict(updated_book) == {"id": 1, **body}

    def test_delete_server_side(self, books):
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
    def test_create_rest(self, benchmark):
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
        response = benchmark(client.post, url, body)

        assert response.status_code is HTTP_201_CREATED

        # read the created book
        new_book = Book.objects.get(pk=1)

        assert model_to_dict(new_book) == {"id": 1, **body}

    def test_read_one_rest(self, benchmark, books):
        """Ensure we can retrieve one book: GET /books/1"""
        client = APIClient()

        url = reverse("book-rest-detail", kwargs={"pk": 1})
        response = benchmark(client.get, url)

        body = {
            "id": 1,
            "title": "Moby Dick",
            "author": "Herman Melville",
            "language": "english",
            "pages": 677,
        }

        assert response.status_code is HTTP_200_OK
        assert response.json() == body

    def test_read_all_rest(self, benchmark, books):
        """Ensure we can list all books: GET /books/"""
        client = APIClient()

        url = reverse("book-rest-list")
        response = benchmark(client.get, url)

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

    def test_update_rest(self, benchmark, books):
        """Ensure we can update a book: PUT /books/1"""
        client = APIClient()

        body = {
            "title": "Moby Dick",
            "author": "Herman Melville",
            "language": "JP",
            "pages": 455,
        }

        url = reverse("book-rest-detail", kwargs={"pk": 1})
        response = benchmark(client.put, url, body)

        assert response.status_code is HTTP_200_OK

        # assert the book was updated
        updated_book = Book.objects.first()

        assert model_to_dict(updated_book) == {"id": 1, **body}

    def test_partial_update_rest(self, benchmark, books):
        """Ensure we can partial update a book: PATCH /books/1"""
        client = APIClient()

        body = {
            "language": "JP",
        }

        url = reverse("book-rest-detail", kwargs={"pk": 1})
        response = benchmark(client.patch, url, body)

        assert response.status_code is HTTP_200_OK

        # assert the book was updated
        updated_book = Book.objects.first()

        assert updated_book.language == body["language"]

    def test_delete_rest(self, books):
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
    def test_visualize_schema(self):
        """Ensure the allowed methods are OPTIONS, GET, HEAD, POST, PUT, PATCH, DELETE"""
        client = GrapheneClient(schema)

        query = """
        query {
            __schema {
                queryType {
                name
                fields {
                    name
                    type {
                    name
                    }
                    args {
                    name
                    }
                }
                
                }
                mutationType {
                name
                    fields {
                    name
                    type {
                    name
                    }
                    args {
                    name
                    }
                }
                }
            }
        }
        """

        result = {
            "data": {
                "__schema": {
                    "queryType": {
                        "name": "BookQuery",
                        "fields": [
                            {
                                "name": "book",
                                "type": {"name": "BookType"},
                                "args": [{"name": "id"}, {"name": "title"}],
                            },
                            {"name": "allBooks", "type": {"name": None}, "args": []},
                        ],
                    },
                    "mutationType": {
                        "name": "Mutations",
                        "fields": [
                            {
                                "name": "createBook",
                                "type": {"name": "CreateBookMutation"},
                                "args": [{"name": "input"}],
                            },
                            {
                                "name": "updateBook",
                                "type": {"name": "UpdateBookMutation"},
                                "args": [{"name": "id"}, {"name": "input"}],
                            },
                            {
                                "name": "deleteBook",
                                "type": {"name": "DeleteBookMutation"},
                                "args": [{"name": "id"}],
                            },
                        ],
                    },
                }
            }
        }

        assert client.execute(query) == result

    def test_create_gql(self, benchmark):
        """Ensure we can create a new book"""
        client = GrapheneClient(schema)

        book = {
            "title": "Moby Dick",
            "author": "Herman Melville",
            "language": "EN",
            "pages": 698,
        }

        variables = {"input": book}

        mutation = """
        mutation createMutation($input: CreateBookInput!) {
                createBook(input: $input) {
                    book {
                        title
                        author
                        language
                        pages
                    }
                }
            }
        """

        result = {"data": OrderedDict([("createBook", {"book": book})])}

        assert benchmark(client.execute, mutation, variable_values=variables) == result

        # read the created book
        new_book = Book.objects.get(pk=1)

        assert model_to_dict(new_book) == {"id": 1, **book}

    def test_read_one_gql(self, benchmark, books):
        """Ensure we can retrieve one book"""
        client = GrapheneClient(schema)

        query = """ 
        query {
            book(id: 1) {
                id
                title
                author
                language
                pages
            }
        }"""

        result = {
            "data": {
                "book": {
                    "id": "1",
                    "title": "Moby Dick",
                    "author": "Herman Melville",
                    "language": "english",
                    "pages": 677,
                }
            }
        }

        assert benchmark(client.execute, query) == result

    def test_read_all_gql(self, benchmark, books):
        """Ensure we can list all books: GET /books/"""
        client = GrapheneClient(schema)

        query = """ 
        query {
            allBooks {
                    id
                    title
                    author
                    language
                    pages
                }
            }"""

        result = {
            "data": {
                "allBooks": [
                    {
                        "id": "1",
                        "title": "Moby Dick",
                        "author": "Herman Melville",
                        "language": "english",
                        "pages": 677,
                    },
                    {
                        "id": "2",
                        "title": "As Crônicas de Nárnia",
                        "author": "C. S. Lewis",
                        "language": "portuguese",
                        "pages": 752,
                    },
                    {
                        "id": "3",
                        "title": "Harry Potter und Der Stein der Weisen",
                        "author": "J. K. Rowling",
                        "language": "german",
                        "pages": 337,
                    },
                    {
                        "id": "4",
                        "title": "羊をめぐる冒険",
                        "author": "Haruki Murakami",
                        "language": "japanese",
                        "pages": 331,
                    },
                ]
            }
        }

        assert benchmark(client.execute, query) == result

    def test_update_gql(self, benchmark, books):
        """Ensure we can partial update a book"""
        client = GrapheneClient(schema)

        variables = {"id": 1, "input": {"language": "JP", "pages": 566}}

        mutation = """
        mutation updateMutation($id: ID!, $input: PatchBookInput!) {
                updateBook(id: $id, input: $input) {
                    book {
                        id
                        title
                        author
                        language
                        pages
                    }
                }
            }
        """

        book = {
            "title": "Moby Dick",
            "author": "Herman Melville",
            "language": "JP",
            "pages": 566,
        }

        result = {"data": OrderedDict([("updateBook", {"book": {"id": "1", **book}})])}

        assert benchmark(client.execute, mutation, variable_values=variables) == result

        # read the updated book
        updated_book = Book.objects.get(pk=1)

        assert model_to_dict(updated_book) == {"id": 1, **book}

    def test_delete_gql(self, books):
        """Ensure we can delete a book"""
        client = GrapheneClient(schema)

        variables = {"id": 1}

        mutation = """
        mutation deleteMutation($id: ID!) {
                deleteBook(id: $id) {
                    found
                    deletedId
                }
            }
        """

        result = {
            "data": OrderedDict([("deleteBook", {"found": True, "deletedId": "1"},)])
        }

        assert client.execute(mutation, variable_values=variables) == result

        # reading the book should fail
        with pytest.raises(Book.DoesNotExist) as excinfo:
            Book.objects.get(pk=1)  # deleted book
            assert excinfo.value == "Book matching query does not exist"
