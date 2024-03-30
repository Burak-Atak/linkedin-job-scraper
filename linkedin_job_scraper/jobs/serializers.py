from rest_framework import serializers
from .enums import WorkType, JobStatus
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    work_type = serializers.ChoiceField(choices=WorkType.choices())
    work_type_display = serializers.CharField(source='get_work_type_display', read_only=True)
    status = serializers.ChoiceField(choices=JobStatus.choices())
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Job
        fields = '__all__'


class JobSerializerDetailed(JobSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        depth = 1
