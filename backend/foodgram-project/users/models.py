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


class Subscription(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Follower",
    )
    follow = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follow",
        verbose_name="Follow",
    )

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "follow"], name="unique_follow"
            )
        ]

    def __str__(self) -> str:
        return f"{self.follower.username} on {self.follow.username}"
