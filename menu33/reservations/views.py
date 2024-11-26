from django.shortcuts import render


def book_a_table(request):
    return render(request, 'reservations/book-a-table.html')
