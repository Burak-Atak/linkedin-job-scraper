from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from address.models import City
from address.service import CityService
from address.serializers import CitySerializer
from address.filters import CityFilter
from api.permissions import IsAuthenticatedOrReadOnly


class CityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cities to be viewed or edited.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    service = CityService()
    filter_backends = [OrderingFilter]
    ordering_fields = '__all__'
    filter_class = CityFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        return self.service.get_or_create_city(serializer.data)
