from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models

user = get_user_model()


class Quote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"Quote(id={self.id}, text={self.text}, created_at={self.created_at})"


class Subquote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="subquotes")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]


class Badge(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Badge(id={self.id}, name={self.name}, description={self.description}, created_at={self.created_at})"
