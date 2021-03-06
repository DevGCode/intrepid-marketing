# Generated by Django 3.1.7 on 2021-03-07 06:36

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.BooleanField(default=False)),
                ('call_list', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('business_name', models.CharField(max_length=100)),
                ('business_type', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=500)),
                ('phone_number', models.CharField(max_length=200)),
                ('note', models.TextField(help_text='Notes')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('cost', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2320)),
                ('current', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=2320)),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='SalesAgent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=660)),
                ('thumbnail', models.ImageField(upload_to='')),
                ('body', ckeditor.fields.RichTextField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=630)),
                ('thumbnail', models.ImageField(upload_to='')),
                ('body', ckeditor.fields.RichTextField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('desc', models.CharField(max_length=300, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.ImageField(upload_to='')),
                ('name', models.CharField(max_length=2320)),
                ('url', models.CharField(max_length=2320)),
            ],
        ),
        migrations.CreateModel(
            name='WebsiteInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=320)),
                ('tagline', models.CharField(max_length=2320)),
                ('description', models.CharField(max_length=9320)),
                ('address', models.CharField(max_length=2320)),
                ('phone', models.CharField(max_length=320)),
                ('email', models.CharField(max_length=320)),
                ('website', models.CharField(max_length=320)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminarea.template')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SupportTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False)),
                ('subject', models.CharField(max_length=2320)),
                ('description', models.CharField(max_length=9320)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('phone_number', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('OPEN', 'OPEN'), ('PAUSED', 'PAUSED'), ('CLOSED', 'CLOSED')], default='OPEN', max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Support_Ticket_Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False)),
                ('subject', models.CharField(max_length=2320)),
                ('description', models.CharField(max_length=9320)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminarea.supportticket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_url', models.CharField(max_length=1920)),
                ('platform', models.CharField(max_length=320)),
                ('website_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminarea.websiteinfo')),
            ],
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('call_date', models.CharField(max_length=100)),
                ('converted', models.BooleanField(default=False)),
                ('read', models.BooleanField(default=False)),
                ('monthly_revenue', models.CharField(max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('CANCELED', 'CANCELED'), ('COMPLETED', 'COMPLETED'), ('REFUNDED', 'REFUNDED'), ('PENDING PAYMENT', 'PENDING PAYMENT')], max_length=200, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminarea.lead')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminarea.product')),
            ],
        ),
        migrations.AddField(
            model_name='lead',
            name='agent',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='adminarea.salesagent'),
        ),
        migrations.AddField(
            model_name='lead',
            name='product',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='adminarea.product'),
        ),
        migrations.CreateModel(
            name='FrequentlyAskedQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=320)),
                ('answer', models.CharField(max_length=1520)),
                ('website_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminarea.websiteinfo')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monday_open', models.CharField(max_length=220)),
                ('monday_closed', models.CharField(max_length=220)),
                ('tuesday_open', models.CharField(max_length=220)),
                ('tuesday_closed', models.CharField(max_length=220)),
                ('wednesday_open', models.CharField(max_length=220)),
                ('wednesday_closed', models.CharField(max_length=220)),
                ('thursday_open', models.CharField(max_length=220)),
                ('thursday_closed', models.CharField(max_length=220)),
                ('friday_open', models.CharField(max_length=220)),
                ('friday_closed', models.CharField(max_length=220)),
                ('saturday_open', models.CharField(max_length=220)),
                ('saturday_closed', models.CharField(max_length=220)),
                ('sunday_open', models.CharField(max_length=220)),
                ('sunday_closed', models.CharField(max_length=220)),
                ('website_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminarea.websiteinfo')),
            ],
        ),
        migrations.CreateModel(
            name='BillingReceipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.CharField(max_length=100)),
                ('read', models.BooleanField(default=False)),
                ('billed_for', models.CharField(max_length=600)),
                ('date', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
