from django.db import models


class Book(models.Model):
    """The book django model"""

    title = models.CharField(max_length=64)
    author = models.CharField(max_length=64)
    pages = models.IntegerField()

    class AvailableLanguages(models.TextChoices):
        ENGLISH = "EN", "english"
        PORTUGUESE = "PT", "portuguese"
        GERMAN = "DE", "german"
        JAPANESE = "JP", "japanese"

    language = models.CharField(max_length=2, choices=AvailableLanguages.choices)

    def __str__(self):
        return self.title

