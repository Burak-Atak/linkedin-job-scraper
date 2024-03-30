from django_filters import rest_framework as filters
from company.models import Company


class CompanyFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Company
        fields = ['name']
