from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .models import Book
from .serializers import BookSerializer


class BookViewSet(ModelViewSet):
    """A simple ViewSet for cruding books."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]