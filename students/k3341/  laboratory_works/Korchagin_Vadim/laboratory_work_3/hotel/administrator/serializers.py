from rest_framework import serializers
from .models import Room, Client, Staff, Stay, CleaningSchedule, CleaningExecution

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class StaySerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(), source='client', write_only=True
    )
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(), source='room', write_only=True
    )

    class Meta:
        model = Stay
        fields = ['stay_id', 'client', 'room', 'client_id', 'room_id',
                  'check_in_date', 'check_out_date']

class CleaningScheduleSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True)
    staff_id = serializers.PrimaryKeyRelatedField(
        queryset=Staff.objects.all(), source='staff', write_only=True
    )
    room = RoomSerializer(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(), source='room', write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = CleaningSchedule
        fields = ['cleaning_schedule_id', 'staff', 'staff_id', 'room', 'room_id',
                  'floor', 'time_and_day_of_week']

class CleaningExecutionSerializer(serializers.ModelSerializer):
    cleaning_schedule = CleaningScheduleSerializer(read_only=True)
    cleaning_schedule_id = serializers.PrimaryKeyRelatedField(
        queryset=CleaningSchedule.objects.all(), source='cleaning_schedule', write_only=True
    )
    staff = StaffSerializer(read_only=True)
    staff_id = serializers.PrimaryKeyRelatedField(
        queryset=Staff.objects.all(), source='staff', write_only=True
    )
    room = RoomSerializer(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(), source='room', write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = CleaningExecution
        fields = ['cleaning_execution_id', 'cleaning_schedule', 'cleaning_schedule_id',
                  'staff', 'staff_id', 'time_and_day_of_week', 'floor', 'room', 'room_id']