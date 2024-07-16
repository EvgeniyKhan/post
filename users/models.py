from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from config.settings import NULLABLE


class CustomUserManager(BaseUserManager):
    """
    Менеджер пользователей с переопределенными методами создания пользователя и суперпользователя.

    Methods:
        create_user: Создает и сохраняет пользователя с указанным номером телефона и паролем.
        create_superuser: Создает и сохраняет суперпользователя с указанным номером телефона и паролем.
    """

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_("Телефон должен быть указан"))
        phone_number = self.normalize_email(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
            Создает и сохраняет суперпользователя с заданными атрибутами.

            Args:
            - phone_number (str): Номер телефона суперпользователя.
            - password (str, optional): Пароль суперпользователя.
            - **extra_fields (dict): Дополнительные атрибуты для создания суперпользователя.

            Returns:
            - User: Созданный объект суперпользователя.

            Raises:
            - ValueError: Если атрибуты is_staff или is_superuser не установлены в True.

        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Суперпользователь должен иметь is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Суперпользователь должен иметь is_superuser=True."))

        return self.create_user(phone_number, password, **extra_fields)


class Subscription(models.Model):
    """
    Модель подписки на блог.

    Attributes:
        content_id (str): Индикатор страйпа.
        payment_data (DateField): Дата оплаты.
        payment_session (str): Сессия платежа.
        payment_url (URLField): Ссылка для оплаты.
        user (ForeignKey): Ссылка на пользователя.
        blog (ForeignKey): Ссылка на блог.

    Meta:
        verbose_name (str): Отображаемое имя модели в единственном числе.
        verbose_name_plural (str): Отображаемое имя модели во множественном числе.
    """

    content_id = models.CharField(
        max_length=300, verbose_name="Индикатор страйпа", **NULLABLE
    )
    payment_data = models.DateField(
        auto_now=True, verbose_name="Дата оплаты", **NULLABLE
    )
    payment_session = models.CharField(
        max_length=300, verbose_name="Сессия платежа", **NULLABLE
    )
    payment_url = models.URLField(
        max_length=400, verbose_name="Ссылка для оплаты", **NULLABLE
    )
    price = models.DecimalField(
        max_digits=4, decimal_places=2, default=5.00, verbose_name="Цена"
    )
    is_subscribed = models.BooleanField(default=False, verbose_name="Подписка")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class User(AbstractBaseUser, PermissionsMixin):
    """
    Пользовательская модель пользователя с телефоном в качестве уникального идентификатора.

    Attributes:
        phone_number (str): Телефон пользователя.
        avatar (ImageField): Аватар пользователя.
        first_name (str): Фамилия пользователя.
        last_name (str): Имя пользователя.
        is_active (bool): Активен ли пользователь.
        is_staff (bool): Является ли пользователь персоналом.
        is_superuser (bool): Является ли пользователь суперпользователем.

    Meta:
        verbose_name (str): Отображаемое имя модели в единственном числе.
        verbose_name_plural (str): Отображаемое имя модели во множественном числе.
    """

    username = None
    phone_number = models.CharField(max_length=40, unique=True, verbose_name="Телефон", validators=[
        RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Номер телефона должен быть в формате: '+999999999'. Допустимая длина от 9 до 15 цифр."
        ),
    ])
    avatar = models.ImageField(
        upload_to="users/", verbose_name="Изображение", **NULLABLE
    )
    first_name = models.CharField(max_length=30, verbose_name="Фамилия", **NULLABLE)
    last_name = models.CharField(max_length=30, verbose_name="Имя", **NULLABLE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    payments = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        verbose_name="Ссылка на пользователя",
        **NULLABLE,
    )

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.phone_number}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
