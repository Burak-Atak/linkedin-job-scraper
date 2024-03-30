from django_filters import rest_framework as filters
from .models import Job
from .enums import JobStatus, WorkType


class JobFilter(filters.FilterSet):
    linkedin_job_id = filters.CharFilter(lookup_expr='exact')
    title = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    work_type = filters.MultipleChoiceFilter(choices=WorkType.choices())
    status = filters.MultipleChoiceFilter(choices=JobStatus.choices())
    date_posted = filters.DateFromToRangeFilter()
    city = filters.NumberFilter(field_name='city__id')
    company = filters.NumberFilter(field_name='company__id')
    city__name = filters.CharFilter(lookup_expr='icontains')
    company__name = filters.CharFilter(lookup_expr='icontains')
