from django.conf import settings
from django.db import models

from config.settings import NULLABLE


class Blog(models.Model):
    """
    Модель блога для хранения статей.

    Attributes:
        title (CharField): Заголовок статьи (максимальная длина 100 символов).
        content (TextField): Содержимое статьи.
        preview (ImageField): Изображение предпросмотра статьи (загружается в папку 'preview/').
        count_view (IntegerField): Количество просмотров статьи (по умолчанию 0).
        created_at (DateField): Дата публикации статьи (автоматически добавляется при создании).
        user (ForeignKey): Владелец статьи (ссылка на модель пользователя из настроек Django).
        price (IntegerField, optional): Цена на подписку (может быть пустым).

    Methods:
        __str__: Возвращает строковое представление объекта, используя заголовок статьи.
    """

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое статьи")
    preview = models.ImageField(
        upload_to="preview/", verbose_name="Изображение", **NULLABLE
    )
    count_view = models.IntegerField(default=0, verbose_name="Количество просмотров")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата публикации")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец", **NULLABLE
    )
    is_premium = models.BooleanField(default=False, verbose_name="Платный контент")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        permissions = [
            ("can_edit_title", "Can edit title"),
            ("can_edit_content", "Can edit content"),
        ]
