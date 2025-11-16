from enum import unique
from django.db import models
from books.models import Book
from django.utils import timezone
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
    current_reading = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    reading_progress = models.IntegerField(default=0)

class userLibrary(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(EldergateLibraryUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    book_type = models.CharField(max_length=100, null=True, blank=True)
    time_read = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    

class Cart(models.Model):
    user = models.OneToOneField(EldergateLibraryUser, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


    