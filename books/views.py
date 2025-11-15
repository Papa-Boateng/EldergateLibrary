from django.shortcuts import render, redirect
from .models import Book, Category, SubCategory
from accounts.models import userLibrary
from .forms import CategoryForm, BookForm, SubcategoryForm, BookSubcategoryForm
from accounts.helpers import book_btn_on_price
from django.http import HttpResponse, JsonResponse

# Create your views here.
def books_category_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-dashboard')
       
    all_categories = Category.objects.all()
    return HttpResponse(all_categories)


def books_subcategory_view(request):
    if request.method == 'POST':
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': "Subcategory added successfully!"}, status=200)
        else:
            return JsonResponse({'error': 'Error adding subcategory.'}, status=400)

    category_filter = request.GET.get('category')
    if category_filter:
        subcategories = SubCategory.objects.filter(category_id=category_filter)
    else:
        subcategories = SubCategory.objects.none() # Return an empty queryset if no category is provided

    data = list(subcategories.values('id','name'))  # Serialize to a list of dictionaries
    return JsonResponse(data, safe=False)

def book_details_view(request, book_id):
    if request.session.get('is_authenticated'):
        user = request.user
        title = "Book Details"
        subtitle = "All the information about the selected book."
        book = Book.objects.get(id=book_id)
        _, book_action_btn, icon = book_btn_on_price(book.price)
        data = {
            'id': book.id,
            'title': book.title,
            'description': book.description,
            'author': book.author,
            'category': book.category.name,
            'category_id': book.category.id,
            'subcategory': book.subcategory.name,
            'subcategory_id': book.subcategory.id,
            'publisher': book.publisher,
            'publication_date': book.publication_date,
            'isbn': book.isbn,
            'pages': book.total_pages,
            'cover': book.cover_image.url,
            'price': book.price,
            'date_created': book.timestamp,
            'file': book.pdf_link.url,
            'action_btn': {
                'text': book_action_btn,
                'icon': icon
            },
        }
        return render(request, 'app/book-details.html', {'user': user, 'book_data': data, 'title': title, 'subtitle': subtitle})
    else:
        return redirect('login')    
   
    

def delete_subcategory_view(request, subcategory_id):
    try:
        subcategory = SubCategory.objects.get(id=subcategory_id)
        if request.method == 'POST':
            subcategory.delete()
            return JsonResponse({'message': 'Subcategory deleted successfully!'}, status=200)
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    except SubCategory.DoesNotExist:
        return JsonResponse({'error': 'Subcategory not found.'}, status=404)

def books_management_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Book saved successfully!'}, status=200)
        else:
            return JsonResponse({'error': 'Error saving book.'}, status=400)
    search_books = request.GET.get('search_books')
    if search_books:
        all_books = Book.objects.filter(title__icontains=search_books)
    else:
        all_books = Book.objects.all()
    data = list(all_books.values())
    return JsonResponse(data, safe=False)

def edit_book_view(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        update_type = request.POST.get('update_type')
        if update_type == 'subcategory':
            form = BookSubcategoryForm(request.POST, instance=book)
        else:
            form = BookForm(request.POST, request.FILES, instance=book)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Book updated successfully!'}, status=200)
        else:
            if update_type == 'subcategory':
                return JsonResponse({'error': 'Error Select a Subcategory.'}, status=400)
            return JsonResponse({'error': 'Error updating book.'}, status=400)

    book_dict = {
        'id': book.id,
        'title': book.title,
        'description': book.description,
        'author': book.author,
        'category': book.category.name,
        'category_id': book.category.id,
        'publisher': book.publisher,
        'publication_date': book.publication_date,
        'isbn': book.isbn,
        'pages': book.total_pages,
        'cover': book.cover_image.url,
        'price': book.price,
        'date_created': book.timestamp,
        'file': book.pdf_link.url
    }
    return JsonResponse(book_dict)

def delete_book_view(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        book.delete()
        return JsonResponse({'message': 'Book deleted successfully!'}, status=200)
    return JsonResponse({'title': book.title}, status=200)

def add_trending_view(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        if book.is_trending:
            return JsonResponse({'error': 'Book is already trending!'}, status=400)
        book.is_trending = True
        book.save()
        return JsonResponse({'message': 'Book added to trending successfully!'}, status=200)
    return JsonResponse({'title': book.title}, status=200)

def remove_trending_view(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        if not book.is_trending:
            return JsonResponse({'error': 'Book is not trending!'}, status=400)
        book.is_trending = False
        book.save()
        return JsonResponse({'message': 'Book removed from trending successfully!'}, status=200)
    return JsonResponse({'title': book.title}, status=200)



### read book view ###
def read_book_view(request, book_id):
    book = Book.objects.get(id=book_id)
    user = request.user

    book_type = request.GET.get('book_type')

    if book_type:
        # Check if the book is already in the user's library, and if not, add it.
        user_library_entry, created = userLibrary.objects.get_or_create(user=user, book=book, defaults={'book_type': book_type})

        if created:
            return JsonResponse({'message': 'Book added to your library successfully!', 'open_book_url': reverse('pdf-viewer', args=[book.id])}, status=200)
        else:
            return JsonResponse({'error': 'Book already in your library!'}, status=400)
    return JsonResponse({'title': book.title}, status=200)
