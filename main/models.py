from django.conf import settings
from django.db import models

from users.models import NULLABLE, User


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название курса')
    preview = models.ImageField(upload_to='preview/', verbose_name='превью курса', **NULLABLE)
    description = models.TextField(verbose_name='описание курса')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name='название урока', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='preview/', verbose_name='превью урока', **NULLABLE)
    video_link = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, verbose_name='курс', related_name='lessons', on_delete=models.CASCADE, **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return self.name


class Payment(models.Model):
    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE,
                             **NULLABLE, related_name='payments')
    payment_date = models.DateField(verbose_name='дата оплаты', auto_now_add=True)

    COURSE_OR_LESSON_CHOICES = [
        ('course', 'Курс'),
        ('lesson', 'Урок'),
    ]

    course_or_lesson = models.CharField(max_length=10, choices=COURSE_OR_LESSON_CHOICES)
    payment_sum = models.DecimalField(max_digits=10, decimal_places=2)

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"{self.user} - {self.payment_sum} - {self.payment_date}"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'





