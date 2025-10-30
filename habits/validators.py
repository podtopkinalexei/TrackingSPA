from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_habit(habit):
    """Валидация привычки"""

    if habit.related_habit and habit.reward:
        raise ValidationError({
            'related_habit': _('Нельзя одновременно указывать связанную привычку и вознаграждение.'),
            'reward': _('Нельзя одновременно указывать связанную привычку и вознаграждение.')
        })

    if habit.related_habit and not habit.related_habit.is_pleasant:
        raise ValidationError({
            'related_habit': _('В связанные привычки можно добавлять только приятные привычки.')
        })

    if habit.is_pleasant:
        if habit.reward:
            raise ValidationError({
                'reward': _('У приятной привычки не может быть вознаграждения.')
            })
        if habit.related_habit:
            raise ValidationError({
                'related_habit': _('У приятной привычки не может быть связанной привычки.')
            })

    if habit.periodicity > 7:
        raise ValidationError({
            'periodicity': _('Периодичность не может быть реже, чем 1 раз в 7 дней.')
        })

