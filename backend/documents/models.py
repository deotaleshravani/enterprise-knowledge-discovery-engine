from django.db import models


class Document(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=100,
    )

    source = models.CharField(max_length=50)

    text = models.TextField()

    author = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    date = models.DateTimeField(
        null=True,
        blank=True
    )

    metadata = models.JSONField(default=dict)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.source} - {self.id}"