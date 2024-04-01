from django.db import models
from enumfields.fields import EnumField
from .enums import WorkType, JobStatus


class Job(models.Model):
    title = models.CharField(max_length=300)
    linkedin_job_id = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey('address.City', on_delete=models.CASCADE, null=True, blank=True)
    work_type = EnumField(WorkType, max_length=30, null=True, blank=True)
    status = EnumField(JobStatus, max_length=30, default=JobStatus.new)
    date_posted = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    url = models.URLField(null=True, blank=True)
    applies = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'jobs'
