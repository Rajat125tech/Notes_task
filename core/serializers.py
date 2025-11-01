from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Note

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email',''),
            password=validated_data['password']
        )
        return user

class NoteSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, allow_null=True)
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'file', 'task', 'created_at']
        read_only_fields = ['id', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'due_date', 'created_at', 'notes']
        read_only_fields = ['id', 'created_at']
