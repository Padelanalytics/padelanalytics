# Coppyright (c) 2020 Francisco Javier Revilla Linares to present.
# All rights reserved.
from django.urls import path
from booking import views

urlpatterns = [
    path('book', views.book, name='book'),
]
