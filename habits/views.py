from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import Habit
from .serializers import HabitSerializer, PublicHabitSerializer
from .pagination import HabitPagination


class HabitListCreateView(generics.ListCreateAPIView):
    """Список и создание привычек текущего пользователя"""
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabitPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['is_pleasant', 'is_public', 'periodicity']
    ordering_fields = ['time', 'created_at', 'updated_at']
    search_fields = ['action', 'place']

    def get_serializer_class(self):
        return HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)



class HabitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, обновление и удаление привычки"""
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    """Список публичных привычек"""
    serializer_class = PublicHabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabitPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['periodicity']
    ordering_fields = ['time', 'created_at']
    search_fields = ['action', 'place', 'user__username']

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).select_related('user')

