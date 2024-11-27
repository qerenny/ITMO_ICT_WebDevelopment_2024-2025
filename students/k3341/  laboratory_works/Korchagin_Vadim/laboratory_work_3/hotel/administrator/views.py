from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Room, Client, Staff, Stay, CleaningSchedule, CleaningExecution
from .serializers import (
    RoomSerializer, ClientSerializer, StaffSerializer, StaySerializer,
    CleaningScheduleSerializer, CleaningExecutionSerializer
)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['room_type', 'floor']
    search_fields = ['phone_number', 'room_id']

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city_of_origin']
    search_fields = ['last_name', 'first_name', 'passport_number']

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['last_name', 'first_name']

class StayViewSet(viewsets.ModelViewSet):
    queryset = Stay.objects.all()
    serializer_class = StaySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['client__client_id', 'room__room_id', 'check_in_date', 'check_out_date']
    search_fields = ['client__last_name', 'room__room_id']

class CleaningScheduleViewSet(viewsets.ModelViewSet):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['staff__staff_id', 'floor', 'time_and_day_of_week']
    search_fields = ['staff__last_name', 'time_and_day_of_week']

class CleaningExecutionViewSet(viewsets.ModelViewSet):
    queryset = CleaningExecution.objects.all()
    serializer_class = CleaningExecutionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['staff__staff_id', 'floor', 'time_and_day_of_week']
    search_fields = ['staff__last_name', 'time_and_day_of_week']