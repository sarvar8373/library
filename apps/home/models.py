# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Genre(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name 

class Shelf(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='genres')
    shelf_number = models.CharField(max_length=11)
    shelf_row = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Javon raqami {self.shelf_number} qatori {self.shelf_row} janri {self.genre.name}"

class Book(models.Model):
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE, related_name='shelfs')
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='static/book_images/')
    count = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    @property
    def available_count(self):
        total_reserved = self.reservations.aggregate(total=Sum('count'))['total'] or 0
        return int(self.count or 0) - total_reserved

    def __str__(self):
        return self.name

class BookReservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    get_name = models.CharField(max_length=255)
    count = models.CharField(max_length=255, null=True, blank=True)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation {self.book.name} on {self.reservation_date}"


