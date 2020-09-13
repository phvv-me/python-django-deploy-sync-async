import os
from random import randint

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'my_django_project.settings'
django.setup()

from django.forms import model_to_dict
from locust import HttpUser, task, between
from django.urls import reverse

from my_books.factories import BookFactory


class ServerSideUser(HttpUser):
    wait_time = between(1, 2)

    @task(2)
    def create(self):
        new_book = BookFactory()
        url = reverse("book-create")

        self.client.post(url, json=model_to_dict(new_book))

    @task(2)
    def read_one(self):
        url = reverse("book-read", kwargs={"pk": self.random_pk})

        self.client.get(url)

    @task(1)
    def read_all(self):
        url = reverse("book-list")
        self.client.get(url)

    @task(1)
    def update(self):
        url = reverse("book-update", kwargs={"pk": self.random_pk})

        new_book = BookFactory()
        self.client.post(url, json=model_to_dict(new_book))

    @task(1)
    def delete(self):
        url = reverse("book-delete", kwargs={"pk": self.random_pk})

        self.client.delete(url)

    @property
    def random_pk(self):
        return randint(1, 15_000)
