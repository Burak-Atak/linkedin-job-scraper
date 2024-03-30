from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    logo = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'company'
