from rest_framework import serializers
from .models import Habit
from .validators import validate_habit
from users.serializers import UserShortSerializer
from django.core.exceptions import ValidationError

class HabitSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def create(self, validated_data):
        # Устанавливаем текущего пользователя
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        # Создаем временный объект привычки для валидации
        habit = Habit(**data)
        habit.user = self.context['request'].user

        # Выполняем валидацию
        try:
            validate_habit(habit)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return data


class PublicHabitSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = Habit
        fields = ('id', 'user', 'place', 'time', 'action', 'periodicity',
                  'time_to_complete', 'created_at')
        read_only_fields = fields



