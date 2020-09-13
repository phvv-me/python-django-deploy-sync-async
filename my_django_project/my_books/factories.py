import string

import factory
from factory.fuzzy import FuzzyText, FuzzyInteger, FuzzyChoice

from .models import Book


class BookFactory(factory.Factory):
    class Meta:
        model = Book

    title = FuzzyText(prefix="Book ", length=10, chars=string.printable)
    author = FuzzyText(length=5, chars=string.ascii_letters)
    pages = FuzzyInteger(100, 1000)
    language = FuzzyChoice(Book.AvailableLanguages.labels)
