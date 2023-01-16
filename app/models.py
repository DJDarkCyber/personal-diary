from django.db import models

# Create your models here.


class Quotes(models.Model):
    usrName = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    quote = models.TextField()
    quotedAt = models.DateTimeField(auto_now_add=True)


class Diary(models.Model):
    addedAt = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=255)
    title = models.TextField()
    diary_content = models.TextField()