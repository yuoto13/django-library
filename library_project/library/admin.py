from django.contrib import admin
from .models import User, Book, BorrowedBook

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'available', 'link')  # Добавляем поле 'link'
    fields = ('title', 'author', 'genre', 'available', 'link')  # Добавляем поле 'link' в форму

class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_date', 'returned_date')
    list_filter = ('user', 'book', 'borrowed_date', 'returned_date')

admin.site.register(User)
admin.site.register(Book, BookAdmin)  # Используем новый класс BookAdmin
admin.site.register(BorrowedBook, BorrowedBookAdmin)
