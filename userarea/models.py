from django.db import models
from datetime import datetime, date
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()



class Report(models.Model):
    date_created = models.DateTimeField(auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    title = models.CharField(max_length=660)
    url = models.FileField()

    def __str__(self):
        return self.title



class Deliverable(models.Model):
    date_created = models.DateTimeField(auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    title = models.CharField(max_length=660)
    url = models.FileField()


    def __str__(self):
        return self.title
