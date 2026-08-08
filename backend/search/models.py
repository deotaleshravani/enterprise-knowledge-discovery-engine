from django.db import models

from documents.models import Document


class Chunk(models.Model):

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="chunks"
    )

    chunk_index = models.IntegerField()

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["chunk_index"]

    def __str__(self):
        return (
            f"{self.document.id}"
            f" - chunk {self.chunk_index}"
        )

class SearchAnalytics(models.Model):
    """
    Stores analytics for every enterprise search.
    """

    query = models.TextField()

    intent = models.CharField(
        max_length=100,
        blank=True,
    )

    source = models.CharField(
        max_length=50,
        blank=True,
    )

    confidence = models.IntegerField(
        default=0,
    )

    retrieved_chunks = models.IntegerField(
        default=0,
    )

    response_time = models.FloatField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.query