from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Кастомная модель пользователя с дополнительным полем для аватара
    и номера телефона пользователя.
    Args:
        image (ImageField): Поле для хранения аватара пользователя.
        phone_number (CharField): Поле для хранения номера телефона.
    """
    image = models.ImageField(upload_to='users_images',
                              blank=True, null=True, verbose_name='Аватар')
    phone_number = models.CharField(max_length=12, blank=True, null=True)

    class Meta():
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
