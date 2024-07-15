from django import forms
from django.contrib.auth.forms import (PasswordResetForm, UserChangeForm,
                                       UserCreationForm)
from django.forms import BooleanField, ModelForm

from users.models import Subscription, User


class StyleFormMixin(forms.Form):
    """
    Миксин для добавления стилевых классов к полям формы.

    Проходит по всем полям формы и добавляет классы для стилизации в зависимости от типа поля.

    Methods:
        __init__: Инициализирует форму и добавляет стилевые классы к полям.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class UserRegisterForm(UserCreationForm, StyleFormMixin):
    """
    Форма регистрации пользователя с добавлением стилевых классов.

    Inherits:
        UserCreationForm: Стандартная форма регистрации пользователя Django.
        StyleFormMixin: Миксин для добавления стилевых классов к полям формы.
    """

    class Meta:
        model = User
        fields = ("phone_number", "password1", "password2")

    def clean_phone_number(self):
        """
        Проверяет уникальность номера телефона пользователя.

        Возвращает очищенное значение номера телефона, если номер уникален.
        Вызывает ValidationError, если пользователь с таким номером телефона уже существует.
        """
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('Пользователь с таким номером телефона уже существует.')
        return phone_number


class UserPasswordRecoveryForm(StyleFormMixin, PasswordResetForm):
    """
    Форма восстановления пароля пользователя с добавлением стилевых классов.

    Inherits:
        PasswordResetForm: Стандартная форма восстановления пароля Django.
        StyleFormMixin: Миксин для добавления стилевых классов к полям формы.
    """

    class Meta:
        model = User
        fields = ("phone_number",)


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """
    Форма профиля пользователя с добавлением стилевых классов.

    Inherits:
        UserChangeForm: Стандартная форма изменения профиля пользователя Django.
        StyleFormMixin: Миксин для добавления стилевых классов к полям формы.
    """

    class Meta:
        model = User
        fields = ("first_name", "last_name", "avatar", "phone_number")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()


class SubscriptionForm(ModelForm, StyleFormMixin):
    """
    Форма подписки с добавлением стилевых классов.

    Inherits:
        ModelForm: Стандартная модельная форма Django.
        StyleFormMixin: Миксин для добавления стилевых классов к полям формы.
    """

    class Meta:
        model = Subscription
        fields = "__all__"
