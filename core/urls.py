"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from tracker.views import home

schema_view = get_schema_view(
    openapi.Info(
        title="Academic Score Tracker API",
        default_version="v1",
        description="Record semesters, courses, compute GPA/CGPA.",
    ),
    public=True,
    permission_classes=[AllowAny],
)

def home(request):
    return JsonResponse({"message": "Welcome to Academic Score Tracker!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/', include('tracker.urls')), # your trackers urls
    path('api/auth/', include('users.urls')), # your auth urls
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]