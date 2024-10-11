from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import GenreForm, BookForm
from .models import Book, Genre


def index(request):
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'bookland_nest/index.html', context)


def all_genres(request):
    genres = Genre.objects.all()

    context = {
        'genres': genres.order_by('name')
    }
    return render(request, 'bookland_nest/genres.html', context)


def one_genre(request, genre_id):
    genre = Genre.objects.get(id=genre_id)

    books = genre.book_set.order_by('-date_added')

    context = {
        'genre': genre,
        'books': books
    }
    return render(request, 'bookland_nest/genre.html', context)


def create_genre(request):
    if request.method != 'POST':
        form = GenreForm()
    else:
        form = GenreForm(data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('bookland_nest:genres')

    context = {
        'form': form
    }
    return render(request, 'bookland_nest/create_genre.html', context)


def create_book(request, genre_id):
    genre = Genre.objects.get(id=genre_id)
    if request.method != 'POST':
        form = BookForm()
    else:
        form = BookForm(data=request.POST)
        if form.is_valid():
            new_book = form.save(commit=False)
            new_book.genre = genre
            new_book.save()
            return redirect('bookland_nest:genre', genre_id)

    context = {
        'form': form,
        'genre': genre
    }
    return render(request, 'bookland_nest/create_book.html', context)


def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    genre = book.genre
    if request.method != 'POST':
        form = BookForm(instance=book)
    else:
        form = BookForm(instance=book, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('bookland_nest:genre', genre_id=genre.id)

    context = {
        'form': form,
        'book': book,
        'genre': genre
    }
    return render(request, 'bookland_nest/edit_book.html', context)