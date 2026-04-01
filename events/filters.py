import django_filters
from .models import Event

class EventFilter(django_filters.FilterSet):
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    date = django_filters.DateFilter(field_name='date', lookup_expr='date')

    class Meta:
        model = Event
        fields = ['location', 'date']