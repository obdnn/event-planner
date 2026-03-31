import rest_framework.generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (UserSerializer,CustomTokenObtainPairSerializer, UserRegisterSerializer,RegistrationSerializer,EventSerializer)
from .models import User, Event, Registration
from .permissions import IsOrganizer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from datetime import datetime, timedelta
from django.utils import timezone


class UserRegisterView(rest_framework.generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOrganizer]
    queryset = Event.objects.all()

    @extend_schema(
        parameters=[
            OpenApiParameter(name='location', description='Filter by location', required=False, type=str),
            OpenApiParameter(name='date', description='Filter by date. Format: YYYY-MM-DD (e.g. 2026-12-01)', required=False, type=str),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Event.objects.all()
        location = self.request.query_params.get('location')
        date_str = self.request.query_params.get('date')

        if location:
            queryset = queryset.filter(location__icontains=location)

        if date_str:
            try:
                naive_datetime = datetime.strptime(date_str, '%Y-%m-%d')
                aware_start = timezone.make_aware(naive_datetime)
                aware_end = aware_start + timedelta(days=1)
                queryset = queryset.filter(
                    date__gte=aware_start,
                    date__lt=aware_end
                )
            except ValueError:
                pass

        return queryset

    def perform_create(self, serializer):
        serializer.save(organizer = self.request.user)


class RegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Registration.objects.all()

    def get_queryset(self):
        return Registration.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)