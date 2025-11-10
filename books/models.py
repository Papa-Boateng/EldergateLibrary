from django.db import models

# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    isbn = models.CharField(max_length=13)
    publisher = models.CharField(max_length=100)
    publication_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    total_pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_trending = models.BooleanField(default=False)
    cover_image = models.ImageField(upload_to='book_covers/')
    pdf_link = models.FileField(upload_to='books/')
    timestamp = models.DateTimeField(auto_now_add=True)