import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def home(request):
    """Главная страница"""
    return render(request, 'web/home.html')


def login_view(request):
    """Страница входа"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Используем API для аутентификации
        response = requests.post(
            f'{request.build_absolute_uri("/")}api/auth/login/',
            data={'username': username, 'password': password}
        )

        if response.status_code == 200:
            data = response.json()
            # Аутентифицируем пользователя в Django
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Сохраняем токен в сессии
                request.session['access_token'] = data['access']
                request.session['refresh_token'] = data['refresh']
                messages.success(request, 'Успешный вход!')
                return redirect('dashboard')

        messages.error(request, 'Неверные учетные данные')

    return render(request, 'web/login.html')


def register_view(request):
    """Страница регистрации"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        telegram_chat_id = request.POST.get('telegram_chat_id', '')

        if password != password_confirm:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'web/register.html')

        # Используем API для регистрации
        response = requests.post(
            f'{request.build_absolute_uri("/")}api/auth/register/',
            data={
                'username': username,
                'email': email,
                'password': password,
                'password_confirm': password_confirm,
                'telegram_chat_id': telegram_chat_id
            }
        )

        if response.status_code == 201:
            messages.success(request, 'Регистрация успешна! Теперь войдите в систему.')
            return redirect('login')
        else:
            errors = response.json()
            for field, error_list in errors.items():
                for error in error_list:
                    messages.error(request, f'{field}: {error}')

    return render(request, 'web/register.html')


@login_required
def dashboard(request):
    """Панель управления - список привычек пользователя"""
    access_token = request.session.get('access_token')

    if not access_token:
        messages.error(request, 'Сессия истекла. Войдите снова.')
        return redirect('login')

    # Получаем привычки через API
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(
        f'{request.build_absolute_uri("/")}api/habits/',
        headers=headers
    )

    habits = []
    if response.status_code == 200:
        habits_data = response.json()
        habits = habits_data.get('results', [])

    context = {
        'habits': habits,
        'user': request.user
    }
    return render(request, 'web/dashboard.html', context)


@login_required
def public_habits(request):
    """Публичные привычки других пользователей"""
    access_token = request.session.get('access_token')

    if not access_token:
        messages.error(request, 'Сессия истекла. Войдите снова.')
        return redirect('login')

    # Получаем публичные привычки через API
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(
        f'{request.build_absolute_uri("/")}api/habits/public/',
        headers=headers
    )

    habits = []
    if response.status_code == 200:
        habits_data = response.json()
        habits = habits_data.get('results', [])

    context = {
        'habits': habits
    }
    return render(request, 'web/public_habits.html', context)


@login_required
def create_habit(request):
    """Создание новой привычки"""
    if request.method == 'POST':
        access_token = request.session.get('access_token')
        headers = {'Authorization': f'Bearer {access_token}'}

        data = {
            'place': request.POST.get('place'),
            'time': request.POST.get('time'),
            'action': request.POST.get('action'),
            'is_pleasant': bool(request.POST.get('is_pleasant')),
            'periodicity': int(request.POST.get('periodicity', 1)),
            'reward': request.POST.get('reward', ''),
            'time_to_complete': int(request.POST.get('time_to_complete', 60)),
            'is_public': bool(request.POST.get('is_public')),
        }

        # Обрабатываем связанную привычку
        related_habit_id = request.POST.get('related_habit')
        if related_habit_id:
            data['related_habit'] = int(related_habit_id)

        response = requests.post(
            f'{request.build_absolute_uri("/")}api/habits/',
            headers=headers,
            data=data
        )

        if response.status_code == 201:
            messages.success(request, 'Привычка успешно создана!')
            return redirect('dashboard')
        else:
            errors = response.json()
            for field, error_list in errors.items():
                for error in error_list:
                    messages.error(request, f'{field}: {error}')

    # Получаем приятные привычки для выбора связанной привычки
    access_token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(
        f'{request.build_absolute_uri("/")}api/habits/',
        headers=headers,
        params={'is_pleasant': 'True'}
    )

    pleasant_habits = []
    if response.status_code == 200:
        habits_data = response.json()
        pleasant_habits = habits_data.get('results', [])

    context = {
        'pleasant_habits': pleasant_habits,
        'periodicity_choices': [
            (1, 'Ежедневно'), (2, 'Раз в 2 дня'), (3, 'Раз в 3 дня'),
            (4, 'Раз в 4 дня'), (5, 'Раз в 5 дней'), (6, 'Раз в 6 дней'),
            (7, 'Раз в неделю')
        ]
    }
    return render(request, 'web/create_habit.html', context)


@login_required
def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('home')
