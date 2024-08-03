from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # Устанавливаем роль суперпользователя

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    role = models.CharField(max_length=30, null=False, blank=False, default='reader')

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    author = models.CharField(max_length=200, verbose_name='Автор')
    genre = models.CharField(max_length=100, verbose_name='Жанр')
    link = models.URLField(null=True, blank=True, verbose_name='Ссылка')
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
        verbose_name_plural = 'Взятые книги'

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    def days_borrowed(self):
        if self.returned_date:
            return (self.returned_date - self.borrowed_date).days
        else:
            return (timezone.now() - self.borrowed_date).days