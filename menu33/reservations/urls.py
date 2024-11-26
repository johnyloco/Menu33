from django.urls import path

from menu33.reservations import views

urlpatterns = [
    path('', views.book_a_table, name='reservations'),
]