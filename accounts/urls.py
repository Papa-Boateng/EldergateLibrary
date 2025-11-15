from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('library/', views.library_view, name='library'),
    path('orders/', views.orders_view, name='orders'),
    path('profile-edit/', views.profile_edit_view, name='profile-edit'),
    path('librarian-dashboard/', views.librarian_dashboard_view, name='librarian-dashboard'),
    path('librarian-book-management/', views.librarian_book_management_view, name='librarian-book-management'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin-dashboard'),
    path('admin-book-management/', views.admin_book_management_view, name='admin-book-management'),
    path('admin-user-management/', views.admin_user_management_view, name='admin-user-management'),
    path('admin-add-librarian/', views.admin_add_librarian_view, name='admin-add-librarian'),
    path('admin-edit-librarian/<int:librarian_id>/', views.admin_edit_librarian_view, name='admin-edit-librarian'),
    path('admin-delete-librarian/<int:librarian_id>/', views.admin_delete_librarian_view, name='admin-delete-librarian'),
    path('logout/', views.logout_view, name='logout'),
    path('pdf-viewer/<int:book_id>/', views.pdf_reader_view, name='pdf-viewer'),
    path('update-progress/', views.update_reading_progress, name='update-progress'),
]