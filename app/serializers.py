from rest_framework import serializers
from .models import User, Topic, Ticket, Career, Enrollment, TicketInsideSprint, Sprint

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'user_type', 'speed')
