from enum import unique
from django.db import models

# Create your models here.
class EldergateLibraryUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = True
    USER_TYPE_CHOICES = [
        ('Reader', 'Reader'),
        ('Librarian', 'Librarian'),
        ('Administrator', 'Administrator'),
    ]
    model_name = models.CharField(
        max_length=100,
        choices=USER_TYPE_CHOICES,
        default='Reader',
    )

