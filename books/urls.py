from django.urls import path   
from . import views

urlpatterns = [
    path('', views.books_management_view, name='books-management'),
    path('category/', views.books_category_view, name='books-category'),
    path('subcategory/', views.books_subcategory_view, name='books-subcategory'),
    path('edit-book/<int:book_id>/', views.edit_book_view, name='edit-book'),
    path('delete-book/<int:book_id>/', views.delete_book_view, name='delete-book'),
    path('add-trending/<int:book_id>/', views.add_trending_view, name='add-trending'),
    path('remove-trending/<int:book_id>/', views.remove_trending_view, name='remove-trending'),
    path('delete-subcategory/<int:subcategory_id>/', views.delete_subcategory_view, name='delete-subcategory'),
]