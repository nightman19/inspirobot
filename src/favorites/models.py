from django.db import models
from django.contrib.auth.models import User


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    quote_text = models.TextField()
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'quote_text', 'author')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.author}"