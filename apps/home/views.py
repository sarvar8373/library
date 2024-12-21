# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.contrib import messages 
from .models import Book, BookReservation, Genre, Shelf
from .forms import BookForm, BookReservationForm, GenreForm, ShelfForm
from datetime import datetime

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required
def book_list(request):
    books = Book.objects.all().order_by('id')
    form = BookForm()

    if request.method == "POST":
        if 'edit-book' in request.POST: 
            book_id = request.POST.get('book_id')
            shelf_id = request.POST.get("shelf")
            book_name = request.POST.get('name')  
            book_description = request.POST.get('description')  
            book_image = request.FILES.get('image')  
            book_count = request.POST.get('count')  
            book = get_object_or_404(Book, id=book_id)

            book.name = book_name
            book.shelf_id = shelf_id
            book.description = book_description
            if book_image:  
                book.image = book_image
            book.count = book_count
            book.save()  

            return redirect('tables') 

        elif 'add-book' in request.POST:  
            form = BookForm(request.POST, request.FILES) 
            if form.is_valid():
                form.save()
                return redirect('tables')

        elif 'delete-book' in request.POST:  
            book_id = request.POST.get('book_id')
            book = get_object_or_404(Book, id=book_id)
            book.delete()
            return redirect('tables')

    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'books': page_obj,
        'form': form,
        'paginator': paginator,
        'page_obj': page_obj,
    }
    return render(request, 'home/tables.html', context)

@login_required
def reservation_list(request):
    reservations = BookReservation.objects.all().order_by('id')
    current_time = datetime.now()
    form = BookReservationForm()

    if request.method == "POST":
        if 'add-reservation' in request.POST:
            form = BookReservationForm(request.POST)
            if form.is_valid():
                try:
                    form.save()  
                    return redirect('tables2') 
                except ValidationError as e:
                    messages.error(request, e.message)  

        elif 'edit-reservation' in request.POST:
            reservation_id = request.POST.get("reservation_id")
            reservation = get_object_or_404(BookReservation, id=reservation_id)

            get_name = request.POST.get("get_name")
            book_id = request.POST.get("book")
            count = request.POST.get("count")
            reservation_date = request.POST.get("reservation_date")
            reservation_time = request.POST.get("reservation_time")

            if book_id:
                reservation.book_id = book_id
            if get_name:
                reservation.get_name = get_name
            if count:
                if int(count) > reservation.book.available_count:
                    messages.error(request, f"Bu kitobning soni {reservation.book.available_count} qolgan.")
                else:
                    reservation.count = count
            if reservation_date:
                reservation.reservation_date = reservation_date
            if reservation_time:
                reservation.reservation_time = reservation_time

            reservation.save()
            return redirect("tables2")

        elif 'delete-reservation' in request.POST:
            reservation_id = request.POST.get('reservation_id')
            reservation = get_object_or_404(BookReservation, id=reservation_id)
            reservation.delete()
            return redirect('tables2')

    # Pagination
    paginator = Paginator(reservations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'reservations': page_obj,
        'form': form,
        'paginator': paginator,
        'page_obj': page_obj,
        'current_time': current_time,
    }
    return render(request, 'home/tables2.html', context)

@login_required
def genre_list(request):
    genres = Genre.objects.all().order_by('id')
    form = GenreForm()

    if request.method == "POST":
        if 'edit-genre' in request.POST: 
            genre_id = request.POST.get('genre_id')  
            genre_name = request.POST.get('name')

            genre = get_object_or_404(Genre, id=genre_id)

            genre.name = genre_name
            genre.save()  

            return redirect('tables3') 

        elif 'add-genre' in request.POST:  
            form = GenreForm(request.POST) 
            if form.is_valid():
                form.save()
                return redirect('tables3')

        elif 'delete-genre' in request.POST:  
            genre_id = request.POST.get('genre_id')
            genre = get_object_or_404(Genre, id=genre_id)
            genre.delete()
            return redirect('tables3')

    paginator = Paginator(genres, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'genres': page_obj,
        'form': form,
        'paginator': paginator,
        'page_obj': page_obj,
    }
    return render(request, 'home/tables3.html', context)

@login_required
def shelf_list(request):
    shelfs = Shelf.objects.all().order_by('id')
    form = ShelfForm()

    if request.method == "POST":
        # Add Reservation
        if 'add-shelf' in request.POST:
            form = ShelfForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('tables4')
            

        elif 'edit-shelf' in request.POST:
            shelf_id = request.POST.get("shelf_id")
            shelf = get_object_or_404(Shelf, id=shelf_id)
            
            # Get form data
            genre_id = request.POST.get("genre")
            shelf_number = request.POST.get("shelf_number")
            shelf_row = request.POST.get("shelf_row")
            
            # Update fields
            if genre_id:
                shelf.genre_id = genre_id
            if shelf_number:
                shelf.shelf_number = shelf_number
            if shelf_row:
                shelf.shelf_row = shelf_row
                
            shelf.save()
            return redirect("tables4")

        # Delete Reservation
        elif 'delete-shelf' in request.POST:
            shelf_id = request.POST.get('shelf_id')
            shelf = get_object_or_404(Shelf, id=shelf_id)
            shelf.delete()
            return redirect('tables4')

    # Pagination
    paginator = Paginator(shelfs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'shelfs': page_obj,
        'form': form,
        'paginator': paginator,
        'page_obj': page_obj,
    }
    return render(request, 'home/tables4.html', context)
