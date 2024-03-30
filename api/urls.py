from rest_framework import routers

from jobs.views import JobViewSet
from address.views import CityViewSet
from company.views import CompanyViewSet

router = routers.DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'cities', CityViewSet)
router.register(r'companies', CompanyViewSet)

urlpatterns = router.urls
