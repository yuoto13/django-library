from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    author = models.CharField(max_length=200, verbose_name='Автор')
    genre = models.CharField(max_length=100, verbose_name='Жанр')
    available = models.BooleanField(default=True, verbose_name='Доступна')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title

class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    borrowed_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата получения')
    returned_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата возврата')

    class Meta:
        verbose_name = 'Взятая книга'
        verbose_name_plural = 'Взятыые книги'

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
