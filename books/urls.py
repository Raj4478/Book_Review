from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('signup/',views.signup, name='signup'),
    path('book/<str:book_id>/', views.book_detail, name='book_detail'),
      path('search/', views.search_books, name='search_books'),
]