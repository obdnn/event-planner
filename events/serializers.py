from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User,Event,Registration
from django.utils import timezone

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'organizer', 'created_at', 'updated_at']
        read_only_fields = ['organizer', 'created_at', 'updated_at']

    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Event date cannot be in the past.")
        return value

class RegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), source='event', write_only=True)

    class Meta:
        model = Registration
        fields = ['id', 'user', 'event', 'event_id', 'registered_at']
        read_only_fields = ['user', 'registered_at']

    def validate(self, attrs):
        event = attrs.get('event')
        user = self.context['request'].user

        if event.organizer == user:
            raise serializers.ValidationError({
                "event": "You are the organizer of this event. You don't need to register."
            })

        if Registration.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError({
                "event": "You are already registered for this event."
            })

        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        login_input = attrs.get('username')
        user = User.objects.filter(email__iexact=login_input).first()
        if not user:
            user = User.objects.filter(username__iexact=login_input).first()
        if user:
            attrs['username'] = user.username
        return super().validate(attrs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email

        return token
