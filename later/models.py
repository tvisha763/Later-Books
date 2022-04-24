from email import message
from enum import auto
from unittest import mock
from django.db import models
from django.forms import CharField


class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=30)
    reading_list = models.JSONField(default={})
    finished = models.JSONField(default={})
    password = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    salt = models.CharField(max_length=1023)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.CharField(max_length=300)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.user.username, self.book_id)