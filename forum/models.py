from django.core.validators import MinValueValidator
from django.db import models

from config.settings import AUTH_USER_MODEL


class Thread(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    likes = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    date_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ('-date_at',)


class Comment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    date_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:10]


class LikeComment(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)


class LikeThread(models.Model):
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
