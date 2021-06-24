from django.db import models
from datetime import datetime, date
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()



class Signup(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class WebsiteAudit(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    website = models.CharField(max_length=220)
    name = models.CharField(max_length=220)
    phone = models.CharField(max_length=220)
    email = models.CharField(max_length=220)

    def __str__(self):
        return self.name



class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username



class Category(models.Model):
    title = models.CharField(max_length=230)

    def __str__(self):
        return self.title



class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = RichTextField(default=False)
    # view_count = models.IntegerField(default = 0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'pk': self.pk
        })

    def get_update_url(self):
        return reverse('post-update', kwargs={
            'pk': self.pk
        })

    def get_delete_url(self):
        return reverse('post-delete', kwargs={
            'pk': self.pk
        })

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()



class Service(models.Model):
    title = models.CharField(max_length=660)
    thumbnail = models.ImageField()
    body = RichTextField(default=False)


    def __str__(self):
        return self.title
