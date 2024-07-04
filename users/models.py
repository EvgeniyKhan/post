from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from blog.models import Blog
from config.settings import NULLABLE


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_('Телефон должен быть указан'))
        phone_number = self.normalize_email(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_superuser=True.'))

        return self.create_user(phone_number, password, **extra_fields)


class Subscription(models.Model):
    content_id = models.CharField(max_length=300, verbose_name="Индикатор страйпа", **NULLABLE)
    payment_data = models.DateField(auto_now=True, verbose_name="Дата оплаты", **NULLABLE)
    payment_session = models.CharField(max_length=300, verbose_name="Сессия платежа", **NULLABLE)
    payment_url = models.URLField(max_length=400, verbose_name="Ссылка для оплаты", **NULLABLE)
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="Ссылка на пользователя", **NULLABLE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Ссылка на блог", **NULLABLE)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    phone_number = models.CharField(max_length=40, unique=True, verbose_name="Телефон")
    avatar = models.ImageField(upload_to="users/", verbose_name="Изображеие", **NULLABLE)
    first_name = models.CharField(max_length=30, verbose_name="Фамилия", **NULLABLE)
    last_name = models.CharField(max_length=30, verbose_name="Имя", **NULLABLE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.phone_number}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

