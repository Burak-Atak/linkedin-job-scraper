from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import replace_query_param, remove_query_param
from rest_framework.views import APIView

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
    queryset = Job.objects.select_related('company', 'city').order_by('-date_posted')
    serializer_class = JobSerializer
    service = JobsService()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = JobFilter
    ordering_fields = '__all__'
    serializer_action_classes = {
        'detailed': JobSerializerDetailed
    }
    permission_classes = [IsAuthenticatedOrReadOnly]

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

    # bulk_update_status
    @action(detail=False, methods=['post'])
    def bulk_update_status(self, request):
        return Response(self.service.bulk_update_status(request.data))


# Template view
class JobTemplateView(APIView):
    queryset = Job.objects.all().select_related('company', 'city').order_by('-modified_at')
    paginator = PageNumberPagination()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request):
        keywords = request.GET.get('keywords')
        if keywords:
            filter_query = Q()
            for keyword in keywords.split(","):
                filter_query |= Q(title__icontains=keyword) | Q(description__icontains=keyword)
            self.queryset = self.queryset.filter(filter_query)
        page = self.paginator.paginate_queryset(self.queryset, request)
        response = self.paginator.get_paginated_response(page)
        request_url = request.build_absolute_uri()
        first = None
        if (self.paginator.page_query_param in request.query_params
                and request.query_params[self.paginator.page_query_param] != "1"):
            first = remove_query_param(request_url, self.paginator.page_query_param)

        last = None
        if self.paginator.page.has_next():
            last = replace_query_param(request_url, self.paginator.page_query_param,
                                       self.paginator.last_page_strings[0])
        response.data['first'] = first
        response.data['last'] = last
        return response
