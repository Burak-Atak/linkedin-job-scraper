"""linkedin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Jobs API",
      default_version='v1',
   ),
   # public=True,
   # permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api/', include('api.urls')),
    path(r'docs/', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
    path(r'accounts/', include('django.contrib.auth.urls')),
    path(r'', include('jobs.urls')),
]
