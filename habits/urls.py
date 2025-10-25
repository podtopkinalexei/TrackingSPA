from django.urls import path
from . import views

app_name = 'habits'

urlpatterns = [
    path('habits/', views.HabitListCreateView.as_view(), name='habit-list-create'),
    path('habits/<int:pk>/', views.HabitRetrieveUpdateDestroyView.as_view(), name='habit-detail'),
    path('habits/public/', views.PublicHabitListView.as_view(), name='public-habit-list'),
]

