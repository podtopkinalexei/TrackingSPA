from celery import shared_task
from django.utils import timezone
from datetime import datetime
import requests
from django.conf import settings
from .models import Habit


@shared_task
def send_telegram_reminder():
    """Отправка напоминаний в Telegram о привычках"""
    now = timezone.now()
    current_time = now.time()

    # Находим привычки, которые нужно выполнить в текущее время
    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute
    ).select_related('user')

    for habit in habits:
        if habit.user.telegram_chat_id:
            send_habit_reminder.delay(habit.id)


@shared_task
def send_habit_reminder(habit_id):
    """Отправка напоминания о конкретной привычке"""
    try:
        habit = Habit.objects.select_related('user').get(id=habit_id)
    except Habit.DoesNotExist:
        return

    if not habit.user.telegram_chat_id:
        return

    message = format_reminder_message(habit)
    send_telegram_message.delay(habit.user.telegram_chat_id, message)


@shared_task
def send_telegram_message(chat_id, message):
    """Отправка сообщения в Telegram"""
    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False


def format_reminder_message(habit):
    """Форматирование сообщения-напоминания"""
    reward_text = ""
    if habit.reward:
        reward_text = f"\n🎁 Вознаграждение: {habit.reward}"
    elif habit.related_habit:
        reward_text = f"\n💫 Приятная привычка: {habit.related_habit.action}"

    return (
        f"🔔 <b>Напоминание о привычке!</b>\n\n"
        f"📝 Действие: {habit.action}\n"
        f"📍 Место: {habit.place}\n"
        f"⏰ Время: {habit.time.strftime('%H:%M')}\n"
        f"⏱️ Время на выполнение: {habit.time_to_complete} секунд"
        f"{reward_text}\n\n"
        f"Удачи! 💪"
    )