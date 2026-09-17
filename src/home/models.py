import secrets

from django.db import models


def generate_short_id():
    return secrets.token_urlsafe(6)


class SharedQuote(models.Model):
    """
    Created lazily the first time a given quote+author is shared —
    not pre-seeded from ZenQuotes. Reused on repeat shares of the
    same quote via get_or_create(quote_text=..., author=...).
    """

    short_id = models.CharField(
        max_length=12, unique=True, default=generate_short_id, editable=False
    )
    quote_text = models.TextField()
    author = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["quote_text", "author"], name="unique_shared_quote"
            )
        ]

    def __str__(self):
        return f"{self.quote_text[:40]} — {self.author}"