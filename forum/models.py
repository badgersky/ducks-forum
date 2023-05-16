from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


class Thread(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    likes = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    comments = models.ForeignKey('Comment', on_delete=models.CASCADE)
    date_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    date_at = models.DateTimeField(auto_now_add=True)


class LikeComment(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class LikeThread(models.Model):
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
