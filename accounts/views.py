from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import ReaderSignUpForm, ReaderProfileEditForm, LibrarianSignUpForm
from .models import EldergateLibraryUser
from books.models import Category, Book
from . import helpers
from django.http import JsonResponse

# Create your views here.
####Authentication Views####
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['is_authenticated'] = True
            if user.model_name == 'Reader':
                return redirect('dashboard')
            elif user.model_name == 'Librarian':
                return redirect('librarian-dashboard')
            elif user.model_name == 'Administrator':
                return redirect('admin-dashboard')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid username or password'})
    return render(request, 'registration/login.html')

def signup_view(request):
    if request.method == 'POST':
        form = ReaderSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='accounts.backends.MultiModelBackend')
            request.session['is_authenticated'] = True
            return redirect('dashboard')
    else:
        form = ReaderSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

####APP MEMBER VIEWS####
def dashboard_view(request):
    if request.session.get('is_authenticated'):
        user = request.user
        title = "Dashboard"
        subtitle = "Welcome back, your library awaits you."
        filter_category = Category.objects.all()
        trending_books = Book.objects.filter(is_trending=True).order_by('-timestamp')[:5]
        trending_books_data = []
        for trending_book in trending_books:
            style_class, style_text, style_book_type = helpers.get_book_type_from_price('reader', trending_book.price)
            category_class = helpers.user_category_class(trending_book.category.name)
            trending_books_data.append({
                'id': trending_book.id,
                'title': trending_book.title,
                'author': trending_book.author,
                'category': trending_book.category.name,
                'price': trending_book.price,
                'cover_image': trending_book.cover_image,
                'price_style': {
                    'class': style_class,
                    'text': style_text,
                    'status': style_book_type
                },
                'category_class': category_class
            })
        return render(request, 'app/dashboard.html', {'user': user, 'title': title, 'subtitle': subtitle, 'filter_category': filter_category, 'trending_books_data': trending_books_data})
    else:
        return redirect('login')
def library_view(request):
    if request.session.get('is_authenticated'):
        user = request.user
        title = "Library"
        subtitle = "Access your saved books here."
        return render(request, 'app/library.html', {'user': user, 'title': title, 'subtitle': subtitle})
    else:
        return redirect('login')
def orders_view(request):
    if request.session.get('is_authenticated'):
        user = request.user
        title = "Orders"
        subtitle = "View and manage your purchased books."
        filter_category = Category.objects.all()
        return render(request, 'app/orders.html', {'user': user, 'title': title, 'subtitle': subtitle, 'filter_category': filter_category})
    else:
        return redirect('login')
def profile_edit_view(request):
    if request.session.get('is_authenticated'):
        user = request.user
        if request.method == 'POST':
            data = {
                'First_Name': request.POST.get('profile-first-name'),
                'Last_Name': request.POST.get('profile-last-name'),
                'email': request.POST.get('profile-email'),
            }

            if (data['First_Name'] == user.First_Name and data['Last_Name'] == user.Last_Name and data['email'] == user.email):
                return JsonResponse({'message': 'No changes made.'}, status=201)
            
            form = ReaderProfileEditForm(data, instance=user)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Changes made successfully.'}, status=200)
            else:
                return JsonResponse({'error': 'Unexpected Issue. Try again Later'}, status=400)
        
        title = "Profile Edit"
        subtitle = "Edit your profile information."
        app_layout = user.model_name
        if app_layout == 'Librarian':
            base_layout = 'librarian_layout.html'
        elif app_layout == 'Administrator':
            base_layout = 'admin_layout.html'
        else:  # Default to Reader
            base_layout = 'layout.html'
        
        return render(request, 'app/profile-edit.html', {'user': user, 'title': title, 'subtitle': subtitle, 'base_layout': base_layout})
    else:
        return redirect('login')

###APP ADMIN VIEWS####
def admin_dashboard_view(request):
    if request.session.get('is_authenticated'):
        user = request.user
        title = "Dashboard"
        subtitle = "Welcome back, your library awaits you."
        categories = Category.objects.all()
        all_books = Book.objects.all()
        recent_books = Book.objects.order_by('-timestamp')[:5]
        books_with_styles = []
        for book in recent_books:
            style_class, style_text, style_book_type = helpers.get_book_type_from_price('admin', book.price)
            books_with_styles.append({
                'book': book,
                'style': {
                    'class': style_class,
                    'text': style_text,
                    'book_type': style_book_type
                }
            })

        return render(request, 'admin/admin-dashboard.html', {'user': user, 'title': title, 'subtitle': subtitle, 'categories': categories, 'all_books': all_books, 'books_with_styles': books_with_styles})
    else:
        return redirect('login')
def admin_book_management_view(request):
    if request.session.get('is_authenticated'):
        all_books = Book.objects.all()
        categories = Category.objects.all()
        total_books = all_books.count()
        book_list_styles = []
        for book in all_books:
            style_class, style_text = helpers.admin_book_management_bt(book.price)
            category_class = helpers.admin_book_management_category(book.category.name)
            book_list_styles.append({
                'book': book,
                'style': {
                    'class': style_class,
                    'text': style_text
                },
                'category_class': category_class
            })
        user = request.user
        title = "Book Management Panel"
        subtitle = "Add, edit, and delete books from the library."
        return render(request, 'admin/admin-book-management.html', {'user': user, 'title': title, 'subtitle': subtitle, 'all_books': all_books, 'total_books': total_books, 'book_list_styles': book_list_styles, 'category_class': category_class, 'categories': categories})
    else:
        return redirect('login')
def admin_user_management_view(request):
    if request.session.get('is_authenticated'):
        all_users = EldergateLibraryUser.objects.filter(model_name='Reader')
        all_librarians = EldergateLibraryUser.objects.filter(model_name='Librarian')
        num_librarians = all_librarians.count()
        num_users = all_users.count()
        user = request.user
        title = "User Management"
        subtitle = "Welcome back, your library awaits you."
        return render(request, 'admin/admin-user-management.html', {'user': user, 'title': title, 'subtitle': subtitle, 'all_users': all_users, 'num_users': num_users, 'all_librarians': all_librarians, 'num_librarians': num_librarians})
    else:
        return redirect('login')

####User Management Views####
def admin_add_librarian_view(request):
    if request.session.get('is_authenticated'):
        if request.method == 'POST':
            form = LibrarianSignUpForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': "Librarian added successfully!"}, status=200)
            else:
                return JsonResponse({'error': 'Error adding librarian.'}, status=400)
        else:
            form = LibrarianSignUpForm()
    else:
        return redirect('login')

# def admin_edit_user_view(request):
#     if request.session.get('is_authenticated'):
#         user = request.user
#         title = "Edit User"
#         subtitle = "Edit user information."
#         return render(request, 'admin/admin-edit-user.html', {'user': user, 'title': title, 'subtitle': subtitle})
#     else:
#         return redirect('login')

def admin_edit_librarian_view(request, librarian_id):
    if request.session.get('is_authenticated'):
        librarian = EldergateLibraryUser.objects.get(id=librarian_id)
        if request.method == 'POST':
            form = LibrarianSignUpForm(request.POST, instance=librarian)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': "Librarian edited successfully!"}, status=200)
            else:
                return JsonResponse({'error': 'Error editing librarian.'}, status=400)
        libarian_dict = {
            'id': librarian.id,
            'username': librarian.username,
            'email': librarian.email,
            'First_Name': librarian.First_Name,
            'Last_Name': librarian.Last_Name,
            'last_login': librarian.last_login,
            'is_active': librarian.is_active,

        }
        return JsonResponse(libarian_dict)
    else:
        return redirect('login')

def admin_delete_librarian_view(request, librarian_id):
    if request.session.get('is_authenticated'):
        librarian = EldergateLibraryUser.objects.get(id=librarian_id)
        if request.method == 'POST':
            librarian.delete()
            return JsonResponse({'message': 'Librarian deleted successfully!'}, status=200)
        return JsonResponse({'name': librarian.First_Name+' '+librarian.Last_Name})
    else:
        return redirect('login')

#######Librarian Views#######
def librarian_dashboard_view(request):
    if request.session.get('is_authenticated'):
        user = request.user
        title = "Dashboard"
        subtitle = "Welcome back, access your shelf and manage your library."
        categories = Category.objects.all()
        trending_books = Book.objects.filter(is_trending=True).order_by('-timestamp')[:5]
        return render(request, 'librarian/librarian-dashboard.html', {'user': user, 'title': title, 'subtitle': subtitle, 'categories': categories, 'trending_books': trending_books})
    else:
        return redirect('login')
def librarian_book_management_view(request):
    if request.session.get('is_authenticated'):
        user = request.user
        title = "Book Management"
        subtitle = "Welcome back, access your shelf and manage your library."
        all_books = Book.objects.all()
        books_data = []
        for book in all_books:
            category_class = helpers.librarian_book_management_category(book.category.name)
            isbn = helpers.isbn_formatter(book.isbn)
            books_data.append({
                'id': book.id,
                'cover_image_url': book.cover_image.url if book.cover_image else '',
                'title': book.title,
                'author': book.author,
                'category_name': book.category.name if book.category else '',
                'subcategory_name': book.subcategory.name if book.subcategory else '',
                'isbn': isbn,
                'date_added': book.timestamp,
                'category_class': category_class,
            })
        categories = Category.objects.all()
        return render(request, 'librarian/librarian-books.html', {'user': user, 'title': title, 'subtitle': subtitle, 'categories': categories, 'books_data': books_data})
    else:
        return redirect('login')

####Logout View####
def logout_view(request):
    if 'is_authenticated' in request.session:
        del request.session['is_authenticated']
    logout(request)
    return redirect('login')

