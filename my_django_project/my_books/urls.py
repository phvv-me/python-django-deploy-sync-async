from django.urls import path

from rest_framework import routers

from .views import BookList, BookCreate, BookRead, BookUpdate, BookDelete
from .viewsets import BookViewSet

router = routers.SimpleRouter()
router.register("books/api", BookViewSet, "book-rest")

urlpatterns = [
    path("books/", BookList.as_view(), name="book-list"),
    path("books/create/", BookCreate.as_view(), name="book-create"),
    path("books/<int:pk>/", BookRead.as_view(), name="book-read"),
    path("books/<int:pk>/update/", BookUpdate.as_view(), name="book-update"),
    path("books/<int:pk>/delete/", BookDelete.as_view(), name="book-delete"),
] + router.urls

