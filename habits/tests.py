from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Habit

User = get_user_model()


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            telegram_chat_id='123456'
        )
        self.client.force_authenticate(user=self.user)

        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='08:00:00',
            action='Читать книгу',
            is_pleasant=True,
            time_to_complete=60,
            is_public=True
        )

        self.useful_habit = Habit.objects.create(
            user=self.user,
            place='Парк',
            time='19:00:00',
            action='Бегать',
            is_pleasant=False,
            related_habit=self.pleasant_habit,
            time_to_complete=120,
            periodicity=1,
            is_public=False
        )

    def test_habit_creation(self):
        """Тест создания привычки"""
        data = {
            'place': 'Спортзал',
            'time': '18:00:00',
            'action': 'Тренироваться',
            'is_pleasant': False,
            'reward': 'Смотреть сериал',
            'time_to_complete': 90,
            'periodicity': 1,
            'is_public': True
        }

        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['action'], 'Тренироваться')

    def test_habit_validation(self):
        """Тест валидации привычки"""
        # Нельзя одновременно указывать связанную привычку и вознаграждение
        data = {
            'place': 'Парк',
            'time': '19:00:00',
            'action': 'Гулять',
            'is_pleasant': False,
            'related_habit': self.pleasant_habit.id,
            'reward': 'Кофе',
            'time_to_complete': 60,
            'periodicity': 1
        }

        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_public_habits_list(self):
        """Тест списка публичных привычек"""
        response = self.client.get('/api/habits/public/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_pagination(self):
        """Тест пагинации"""
        # Создаем еще несколько привычек
        for i in range(10):
            Habit.objects.create(
                user=self.user,
                place=f'Место {i}',
                time='09:00:00',
                action=f'Действие {i}',
                is_pleasant=False,
                time_to_complete=60,
                periodicity=1
            )

        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(len(response.data['results']), 5)

