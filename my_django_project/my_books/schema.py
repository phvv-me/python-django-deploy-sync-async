from django.forms import ModelForm

from graphene import ObjectType, Schema, Field, Int, String
from graphene_django import DjangoObjectType, DjangoListField
from graphene_django.rest_framework.mutation import SerializerMutation
from graphene_django_cud.mutations import (
    DjangoCreateMutation,
    DjangoPatchMutation,
    DjangoDeleteMutation,
)

from .models import Book
from .serializers import BookSerializer


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        convert_choices_to_enum = False


class BookQuery(ObjectType):
    book = Field(BookType, id=Int(), title=String())
    all_books = DjangoListField(BookType)

    def resolve_book(self, info, **kwargs):
        if _id := kwargs.get("id") is not None:
            return Book.objects.get(pk=_id)

        if title := kwargs.get("title") is not None:
            return Book.objects.get(title=title)

        return None


class CreateBookMutation(DjangoCreateMutation):
    class Meta:
        model = Book


class UpdateBookMutation(DjangoPatchMutation):
    class Meta:
        model = Book


class DeleteBookMutation(DjangoDeleteMutation):
    class Meta:
        model = Book


class Mutations(ObjectType):
    create_book = CreateBookMutation.Field()
    update_book = UpdateBookMutation.Field()
    delete_book = DeleteBookMutation.Field()


schema = Schema(query=BookQuery, mutation=Mutations)

