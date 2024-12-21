# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('tables', views.book_list, name='tables'),
    path('tables2', views.reservation_list, name='tables2'),
    path('tables3', views.genre_list, name='tables3'),
    path('tables4', views.shelf_list, name='tables4'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
