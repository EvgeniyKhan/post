from django.conf import settings
from django.db import models

from config.settings import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое статьи')
    preview = models.ImageField(upload_to='preview/', verbose_name='Изображение', **NULLABLE)
    count_view = models.IntegerField(default=0, verbose_name='Количество просмотров')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец")
    price = models.IntegerField(verbose_name='Цена на подписку', **NULLABLE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, verbose_name="Дата создания коментария")
    comment = models.CharField(max_length=500, verbose_name="Текст коментария")

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
