from django import forms
from .models import Category, Book, SubCategory

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def save(self, commit=True):
        category = super().save(commit=False)
        if commit:
            category.save()
        return category

class SubcategoryForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
    class Meta:
        model = SubCategory
        fields = ['name', 'category']

    def save(self, commit=True):
        subcategory = super().save(commit=False)
        if commit:
            subcategory.save()
        return subcategory

class BookForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)

    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'isbn', 'publisher', 'publication_date', 'category', 'total_pages', 'price', 'cover_image', 'pdf_link']

    def save(self, commit=True):
        book = super().save(commit=False)
        if commit:
            book.save()
        return book
        