from django import forms
from django.contrib.auth.forms import (PasswordResetForm, UserChangeForm,
                                       UserCreationForm)
from django.forms import BooleanField, ModelForm

from users.models import User, Subscription


class StyleFormMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'from-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(UserCreationForm, StyleFormMixin):
    class Meta:
        model = User
        fields = ('phone_number', 'password1', 'password2')


class UserPasswordRecoveryForm(StyleFormMixin, PasswordResetForm):
    class Meta:
        model = User
        fields = ('phone_number',)


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class SubscriptionForm(ModelForm, StyleFormMixin):
    class Meta:
        model = Subscription
        fields = '__all__'
