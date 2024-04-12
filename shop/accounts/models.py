from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


def profile_avatar_directory_path(instance, filename: str) -> str:
    path = "accounts/profile_{pk}/avatar/{filename}".format(
        pk=instance.pk, filename=filename
    )
    return path


class Avatar(models.Model):
    """Модель для хранения аватара пользователя"""

    src = models.ImageField(
        upload_to="accounts/avatars/user_avatars/",
        default="accounts/avatars/default.png",
        verbose_name="Ссылка",
    )
    alt = models.CharField(
        max_length=128, verbose_name="Описание", default="Без описания"
    )

    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватары"


class Profile(AbstractUser):
    """Модель профиля пользователя"""

    id = models.AutoField(primary_key=True)
    fullName = models.CharField(max_length=128, verbose_name="Полное имя")
    phone = models.PositiveIntegerField(
        blank=True, null=True, unique=True, verbose_name="Номер телефона"
    )
    city = models.CharField(verbose_name="Город", max_length=20, default="")
    address = models.CharField(verbose_name="Адрес", max_length=20, default="")
    balance = models.DecimalField(
        decimal_places=2, max_digits=10, default=0, verbose_name="Баланс"
    )
    avatar = models.ForeignKey(
        Avatar,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Аватар",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
