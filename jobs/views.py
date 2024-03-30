from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from api.permissions import IsAuthenticatedOrReadOnly
from .models import Job
from .service import JobsService
from .serializers import JobSerializer, JobSerializerDetailed
from .filters import JobFilter


# Create your views here.

class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows jobs to be viewed or edited.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    service = JobsService()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filter_class = JobFilter
    ordering_fields = '__all__'
    serializer_action_classes = {
        'detailed': JobSerializerDetailed
    }
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Return the list of items for this view.
        """
        queryset = self.queryset

        if self.action == 'detailed':
            queryset = Job.objects.select_related('company', 'city')

        return queryset

    def get_serializer_class(self):
        """
        Return the serializer class based on the action.
        """
        return self.serializer_action_classes.get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        return self.service.create_job(serializer.data)

    @action(detail=False, methods=['get'])
    def detailed(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
