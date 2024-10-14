from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from .forms import GenreForm, BookForm
from .models import Book, Genre


def index(request):
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'bookland_nest/index.html', context)


@login_required
def all_genres(request):
    # genres = Genre.objects.all()
    genres = Genre.objects.filter(owner=request.user)

    context = {
        'genres': genres.order_by('name')
    }
    return render(request, 'bookland_nest/genres.html', context)


@login_required
def one_genre(request, genre_id):
    genre = Genre.objects.get(id=genre_id)

    if genre.owner != request.user:
        raise Http404

    books = genre.book_set.order_by('-date_added')

    context = {
        'genre': genre,
        'books': books
    }
    return render(request, 'bookland_nest/genre.html', context)


@login_required
def create_genre(request):
    if request.method != 'POST':
        form = GenreForm()
    else:
        form = GenreForm(data=request.POST)

        if form.is_valid():
            new_genre = form.save(commit=False)
            new_genre.owner = request.user
            new_genre.save()
            return redirect('bookland_nest:genres')

    context = {
        'form': form
    }
    return render(request, 'bookland_nest/create_genre.html', context)


@login_required
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


@login_required
def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    genre = book.genre

    if genre.owner != request.user:
        raise Http404

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


def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    genre = book.genre

    if genre.owner != request.user:
        raise Http404

    if request.method == 'POST':
        book.delete()
        return redirect('bookland_nest:genre', genre_id=genre.id)
    elif request.method == 'GET':
        context = {
            'book': book,
            'genre': genre
        }
        return render(request, 'bookland_nest/delete_book.html', context)