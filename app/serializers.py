from rest_framework import serializers
from .models import User, Topic, Ticket, Career, Enrollment, TicketInsideSprint, Sprint

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name', 'user_type', 'speed')

class SimplifiedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', )

class SimplifiedTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'name')

class TicketInsideSprintSerializer(serializers.ModelSerializer):
    ticket = SimplifiedTicketSerializer()
    class Meta:
        model = TicketInsideSprint
        fields = ('ticket', 'progress')

class SprintSerializer(serializers.ModelSerializer):
    tickets = TicketInsideSprintSerializer(many=True)
    class Meta:
        model = Sprint
        fields = ('id', 'beginning', 'tickets')

class SimplifiedCareerSerializer(serializers.ModelSerializer):
    author = SimplifiedUserSerializer()
    class Meta:
        model = Career
        fields = ('id', 'name', 'author', 'estimated_time')

class UserEnrollmentSerializer(serializers.ModelSerializer):
    career = SimplifiedCareerSerializer()
    sprints = SprintSerializer(many=True)

    class Meta:
        model = Enrollment
        fields = ('id', 'career', 'sprints')

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'importance', 'estimated_time', 'dependencies')

class CareerSerializer(serializers.ModelSerializer):
    author = SimplifiedUserSerializer()
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Career
        fields = ('id', 'name', 'description', 'author', 'estimated_time', 'tickets')