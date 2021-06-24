from django.db import models
from datetime import datetime, date
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()



class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    cost = models.FloatField(null=True)

    def __str__(self):
        return self.name



class WebsiteInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=320)
    tagline = models.CharField(max_length=2320)
    description = models.CharField(max_length=9320)
    address = models.CharField(max_length=2320)
    phone = models.CharField(max_length=320)
    email = models.CharField(max_length=320)
    website = models.CharField(max_length=320)

    def __str__(self):
        return self.business_name

    def get_absolute_url(self):
        return reverse('info-detail', kwargs={
            'pk': self.pk
        })



class SocialLink(models.Model):
    website_info = models.ForeignKey(WebsiteInfo, on_delete=models.CASCADE)
    social_url = models.CharField(max_length=1920)
    platform = models.CharField(max_length=320)

    def __str__(self):
        return self.platform



class BusinessHours(models.Model):
    monday_open = models.CharField(max_length=220)
    monday_closed = models.CharField(max_length=220)
    tuesday_open = models.CharField(max_length=220)
    tuesday_closed = models.CharField(max_length=220)
    wednesday_open = models.CharField(max_length=220)
    wednesday_closed = models.CharField(max_length=220)
    thursday_open = models.CharField(max_length=220)
    thursday_closed = models.CharField(max_length=220)
    friday_open = models.CharField(max_length=220)
    friday_closed = models.CharField(max_length=220)
    saturday_open = models.CharField(max_length=220)
    saturday_closed = models.CharField(max_length=220)
    sunday_open = models.CharField(max_length=220)
    sunday_closed = models.CharField(max_length=220)
    website_info = models.ForeignKey(WebsiteInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.website_info.business_name



class FrequentlyAskedQuestion(models.Model):
    website_info = models.ForeignKey(WebsiteInfo, on_delete=models.CASCADE)
    question = models.CharField(max_length=320)
    answer = models.CharField(max_length=1520)

    def __str__(self):
        return self.website_info.business_name



class SupportTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    subject = models.CharField(max_length=2320)
    description = models.CharField(max_length=9320)
    timestamp = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=200)
    status = models.CharField(max_length=200, null=True, choices=(
        ('OPEN','OPEN'),
        ('PAUSED','PAUSED'),
        ('CLOSED','CLOSED'),
    )
    , default='OPEN')


    def __str__(self):
        return self.user.username



class Template(models.Model):
    thumbnail = models.ImageField()
    name = models.CharField(max_length=2320)
    url = models.CharField(max_length=2320)

    def __str__(self):
        return self.name



class UserTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)

    def __str__(self):
        return self.template.name



class Promo(models.Model):
    code = models.CharField(max_length=2320)
    current = models.BooleanField(default=False)
    description = models.CharField(max_length=2320)
    end_date = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.description



class Support_Ticket_Response(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    subject = models.CharField(max_length=2320)
    description = models.CharField(max_length=9320)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticket.subject



class BillingReceipt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cost = models.CharField(max_length=100)
    read = models.BooleanField(default=False)
    billed_for = models.CharField(max_length=600)
    date = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username



class Referral(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    call_date = models.CharField(max_length=100)
    converted = models.BooleanField(default=False)
    # Mark as unread once the referral converts to a client
    read = models.BooleanField(default=True)
    monthly_revenue = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username



class SalesAgent(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Lead(models.Model):
    agent = models.ForeignKey(SalesAgent, on_delete=models.CASCADE, default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    # Save the time the lead became a customer
    customer = models.BooleanField(default=False)
    # This will remove the lead from all lists
    call_list = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    business_name = models.CharField(max_length=100)
    business_type = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=200)
    note = models.TextField()
    # Time they became a lead
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '#{0} - {1}'.format(self.id, self.name)

    def get_absolute_url(self):
        return reverse('dashboard')



# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=200, null=True)
    desc = models.CharField(max_length=300, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)



# ORDERING
class Order(models.Model):
    customer = models.ForeignKey(Lead, null=True, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=(
        ('CANCELED','CANCELED'),
        ('COMPLETED','COMPLETED'),
        ('REFUNDED','REFUNDED'),
        ('PENDING PAYMENT','PENDING PAYMENT'),
    ))
