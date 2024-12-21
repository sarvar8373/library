from django import forms
from .models import Book, BookReservation, Genre, Shelf

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
        labels = {
            'name': "Janr nomi",  
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Janr nomini kiriting',  
            }),
        }

class ShelfForm(forms.ModelForm):
    class Meta:
        model = Shelf
        fields = ['genre', 'shelf_number', 'shelf_row']
        widgets = {
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'shelf_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Javon raqami', 
            }),
            'shelf_row': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Javon qatori', 
            }),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['shelf', 'name', 'description', 'count', 'image']  # Removed 'created_at' from fields, as it's auto-generated
        labels = {
            'shelf': "Javon",
            'name': "Kitob nomi",  
            'description': "Kitob matni",
            'count': "Kitob Soni",  
            'image': "Rasmi",
        }
        widgets = {
            'shelf': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Kitob nomini kiriting',  # Placeholder for user guidance
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Kitob haqida matnni kiriting',  # Placeholder for user guidance
            }),
             'count': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Kitob sonini kiriting',  # Placeholder for user guidance
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',  # Bootstrap class for file input
            }),
        }

class BookReservationForm(forms.ModelForm):
    class Meta:
        model = BookReservation
        fields = ['book', 'get_name', 'count', 'reservation_date', 'reservation_time']
        widgets = {
            'reservation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reservation_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'book': forms.Select(attrs={'class': 'form-control'}),
            'get_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Kitob olgan shaxs',  # Placeholder for user guidance
            }),
            'count': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Olingan kitob soni',  # Placeholder for user guidance
            }),
        }