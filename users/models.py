from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    telegram_chat_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('Telegram Chat ID'),
        help_text=_('ID чата в Telegram для отправки уведомлений')
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('Телефон')
    )

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.email})"

