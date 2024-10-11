from django.urls import path
from . import views

app_name = 'bookland_nest'
urlpatterns = [
    path('', views.index, name='index'),
    path('genres/', views.all_genres, name='genres'),
    path('genres/<int:genre_id>', views.one_genre, name='genre'),
    path('new_genre/', views.create_genre, name='create_genre'),
    path('new_book/<int:genre_id>', views.create_book, name='create_book'),
    path('edit_book/<int:book_id>', views.edit_book, name='edit_book'),
]