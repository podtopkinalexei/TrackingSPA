from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from users.models import User


class Habit(models.Model):
    PERIODICITY_CHOICES = [
        (1, 'Ежедневно'),
        (2, 'Раз в 2 дня'),
        (3, 'Раз в 3 дня'),
        (4, 'Раз в 4 дня'),
        (5, 'Раз в 5 дней'),
        (6, 'Раз в 6 дней'),
        (7, 'Раз в неделю'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name=_('Пользователь')
    )
    place = models.CharField(
        max_length=255,
        verbose_name=_('Место'),
        help_text=_('Место, в котором необходимо выполнять привычку')
    )
    time = models.TimeField(
        verbose_name=_('Время выполнения'),
        help_text=_('Время, когда необходимо выполнять привычку')
    )
    action = models.CharField(
        max_length=500,
        verbose_name=_('Действие'),
        help_text=_('Конкретное действие, которое представляет собой привычка')
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name=_('Признак приятной привычки'),
        help_text=_('Привычка, которую можно привязать к выполнению полезной привычки')
    )
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='related_habits',
        verbose_name=_('Связанная привычка'),
        help_text=_('Приятная привычка, связанная с выполнением полезной привычки')
    )
    periodicity = models.PositiveSmallIntegerField(
        choices=PERIODICITY_CHOICES,
        default=1,
        verbose_name=_('Периодичность'),
        help_text=_('Периодичность выполнения привычки в днях'),
        validators=[MinValueValidator(1), MaxValueValidator(7)]
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Вознаграждение'),
        help_text=_('Чем пользователь должен себя вознаградить после выполнения')
    )
    time_to_complete = models.PositiveIntegerField(
        verbose_name=_('Время на выполнение (в секундах)'),
        help_text=_('Время, которое предположительно потратит пользователь на выполнение привычки'),
        validators=[MinValueValidator(1), MaxValueValidator(120)]
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name=_('Признак публичности'),
        help_text=_('Привычка публична и видна другим пользователям')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    class Meta:
        verbose_name = _('Привычка')
        verbose_name_plural = _('Привычки')
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                check=models.Q(time_to_complete__lte=120),
                name='time_to_complete_lte_120'
            ),
            models.CheckConstraint(
                check=models.Q(periodicity__gte=1, periodicity__lte=7),
                name='periodicity_range_1_7'
            ),
        ]

    def __str__(self):
        return f"{self.user.username}: {self.action} в {self.time}"

    def clean(self):
        from .validators import validate_habit
        validate_habit(self)

