from django.db import models

from users.models import NULLABLE


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название курса')
    preview = models.ImageField(upload_to='preview/', verbose_name='превью курса', **NULLABLE)
    description = models.TextField(verbose_name='описание курса')

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

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return self.name
