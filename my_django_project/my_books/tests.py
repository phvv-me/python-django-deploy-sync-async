from django.test import TestCase


def test_this():
    assert True


# Create your tests here.
class TestBooksServerSide:
    def __init__(self):
        # create client
        pass

    def test_create(self):
        """Ensure we can create a new book."""
        assert False

    def test_read(self, books):
        """Ensure we can read the book data."""
        assert False

    def test_read_all(self, books):
        """Ensure we can see a list of all the books."""
        assert False

    def test_update(self, books):
        """Ensure we can update a book."""
        assert False

    def test_delete(self, books):
        """Ensure we can delete a book."""
        assert False


class TestBooksREST:
    def __init__(self):
        # create client
        pass

    def test_identify_options(self):
        """Ensure the allowed methods are OPTIONS, GET, HEAD, POST, PUT, PATCH, DELETE"""
        assert False

    def test_retrieve_one(self, books):
        """Ensure we can retrieve one book: GET /books/1"""
        assert False

    def test_list_all(self, books):
        """Ensure we can list all books: GET /books/"""
        assert False

    def test_create(self):
        """Ensure we can create a new book: POST /books/"""
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


class TestBooksGraphQL:
    def __init__(self):
        # create client
        pass

    def test_identify_options(self):
        assert False

    def test_retrieve_one(self, books):
        assert False

    def test_list_all(self, books):
        assert False

    def test_create(self):
        assert False

    def test_update(self, books):
        assert False

    def test_delete(self, books):
        assert False
