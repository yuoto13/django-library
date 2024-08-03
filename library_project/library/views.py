# library/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import Book, BorrowedBook, User

def home(request):
    return render(request, 'library/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'reader'
            user.save()
            login(request, user)
            return redirect('catalog')
    else:
        form = CustomUserCreationForm()
    return render(request, 'library/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('catalog')
    else:
        form = AuthenticationForm()
    return render(request, 'library/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def catalog(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'library/catalog.html', {'books': books})

@login_required
def my_books(request):
    borrowed_books = BorrowedBook.objects.filter(user=request.user, returned_date__isnull=True).order_by('book__title')
    return render(request, 'library/my_books.html', {'borrowed_books': borrowed_books})

@login_required
def borrow_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.available:
        BorrowedBook.objects.create(user=request.user, book=book)
        book.available = False
        book.save()
    return redirect('catalog')

def return_book(request, book_id):
    borrowed_books = BorrowedBook.objects.filter(book_id=book_id, user=request.user, returned_date__isnull=True)
    for borrowed_book in borrowed_books:
        borrowed_book.returned_date = timezone.now()
        borrowed_book.book.available = True
        borrowed_book.book.save()
        borrowed_book.save()
    return redirect('my_books')

# Новое представление для списка должников
@user_passes_test(lambda u: u.role == 'librarian')
def debtors_list(request):
    debtors = BorrowedBook.objects.filter(returned_date__isnull=True).select_related('user', 'book')
    return render(request, 'library/debtors_list.html', {'debtors': debtors})

def return_book(request, book_id):
    try:
        borrowed_book = BorrowedBook.objects.get(book_id=book_id, user=request.user, returned_date__isnull=True)
        borrowed_book.returned_date = timezone.now()
        borrowed_book.book.available = True
        borrowed_book.book.save()
        borrowed_book.save()
    except BorrowedBook.DoesNotExist:
        pass
    return redirect('my_books')
