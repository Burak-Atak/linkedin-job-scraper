from django.urls import path

from . import views

urlpatterns = [
    path('', views.JobTemplateView.as_view(), name='index'),
]
