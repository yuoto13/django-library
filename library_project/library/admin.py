from django.contrib import admin
from .models import User, Book, BorrowedBook

class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_date', 'returned_date')
    list_filter = ('user', 'book', 'borrowed_date', 'returned_date')

admin.site.register(User)
admin.site.register(Book)
admin.site.register(BorrowedBook, BorrowedBookAdmin)