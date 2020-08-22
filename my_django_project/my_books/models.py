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
        FRENCH = "FR", "french"
        SPANISH = "SP", "spanish"
        GREEK = "GR", "greek"
        ARABIC = "AR", "arabic"
        DUTCH = "NL", "dutch"
        CHINESE = "ZH", "chinese"
        LATIN = "LA", "latin"
        SERBIAN = "SE", "serbian"
        ITALIAN = "IT", "italian"
        RUSSIAN = "RU", "russian"
        MALAY = "MA", "malay"
        GALICIAN = "GA", "galician"
        WELSH = "WL", "welsh"
        SWEDISH = "SW", "swedish"
        NORWEGIAN = "NO", "norwegian"
        TURKISH = "TU", "turkish"
        GAELIC = "GL", "gaelic"
        ALEUT = "AL", "aleut"
        MULTIPLE_LANGUAGES = "MU", "multiple languages"

    language = models.CharField(max_length=2, choices=AvailableLanguages.choices)

    def __str__(self):
        return self.title

