from django.urls import path
from rest_framework import routers

from jobs.views import JobViewSet
from address.views import CityViewSet
from company.views import CompanyViewSet
from api.views import TaskView, CronJobsView

router = routers.DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'cities', CityViewSet)
router.register(r'companies', CompanyViewSet)

urlpatterns = [
    path('run-task/', TaskView.as_view(), name='run-task'),
    path('cron-jobs/', CronJobsView.as_view(), name='cron-jobs'),
]

urlpatterns += router.urls
