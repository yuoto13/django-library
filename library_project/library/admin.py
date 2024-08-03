from django.contrib import admin
from .models import User, Book, BorrowedBook

class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_date', 'returned_date', 'days_borrowed')
    list_filter = ('user', 'book', 'borrowed_date', 'returned_date')

    def days_borrowed(self, obj):
        return obj.days_borrowed()
    days_borrowed.short_description = 'Количество дней'

admin.site.register(User)
admin.site.register(Book)
admin.site.register(BorrowedBook, BorrowedBookAdmin)