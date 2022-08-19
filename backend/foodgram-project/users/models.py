from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    first_name = models.CharField(
        "first name", max_length=150, blank=False, null=False
    )
    last_name = models.CharField(
        "last name", max_length=150, blank=False, null=False
    )
    email = models.EmailField(
        "email address",
        blank=False,
        null=False,
        unique=True,
        max_length=254,
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["username"]

    def __str__(self):
        return self.username
