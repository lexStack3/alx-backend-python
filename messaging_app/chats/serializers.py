from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message, Conversation

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """."""
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['user_id', 'email', 'password', 'password2',
                  'first_name', 'last_name', 'phone_number', 'role']
        read_only_fields = ['user_id']

    def validate(self, attrs):
        """Validates that passwords match."""
        if attrs['password'] != attr['password2']:
            raise serializers.ValidationError({
                'password': "Passwords do not match."
            })
        return attrs

    def create(self, validated_data):
        """Create a <User> instance and sets password."""
        password = validated_data.pop('password')
        validated_data.pop('password2')

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='sender'
    )

    class Meta:
        model = Message
        fields = [
            'message_id', 'conversation',
            'sender', 'sender_id',
            'message_body', 'sent_at'
        ]
        read_only_fields = [
            'message_id', 'sent_at', 'sender'
        ]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participants_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True,
        queryset=User.objects.all(),
        source='participants'
    )
    messages = MessageSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'participants_ids',
            'created_at'
        ]
        read_only_fields = [
            'conversation_id',
            'created_at'
        ]
