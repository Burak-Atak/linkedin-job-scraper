from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from company.models import Company
from company.service import CompanyService
from company.serializers import CompanySerializer
from company.filters import CompanyFilter
from api.permissions import IsAuthenticatedOrReadOnly



class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows companies to be viewed or edited.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    service = CompanyService()
    filter_backends = [OrderingFilter]
    ordering_fields = '__all__'
    filter_class = CompanyFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        return self.service.get_or_create_company(serializer.data)
