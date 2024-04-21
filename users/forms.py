from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, UserChangeForm)

from users.models import User


class UserLoginForm(AuthenticationForm):
    """
    Форма для аутентификации пользователей, основанная на модели User.

    Args:
        username (CharField): Поле для ввода имени пользователя.
        password (CharField): Поле для ввода пароля пользователя.
    """

    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    """
    Форма для регистрации пользователей, основанная на модели User.

    Args:
        first_name (CharField): Поле для ввода имени пользователя.
        last_name (CharField): Поле для ввода фамилии пользователя.
        username (CharField): Поле для ввода уникального имени пользователя.
        email (CharField): Поле для ввода электронной почты пользователя.
        password1 (CharField): Поле для ввода пароля пользователя.
        password2 (CharField): Поле для подтверждения пароля пользователя.
    """
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        )


class ProfileForm(UserChangeForm):
    """
    Форма для редактирования профиля пользователя, основанная на модели User.

    Args:
        image (ImageField): Поле для загрузки изображения профиля пользователя.
        first_name (CharField): Поле для ввода имени пользователя.
        last_name (CharField): Поле для ввода фамилии пользователя.
        username (CharField): Поле для ввода уникального имени пользователя.
        email (CharField): Поле для ввода электронной почты пользователя.
    """
    class Meta:
        model = User
        fields = (
            'image',
            'first_name',
            'last_name',
            'username',
            'email',
        )

    image = forms.ImageField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
