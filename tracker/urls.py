from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SemesterViewSet, CourseViewSet, summary

router = DefaultRouter()
router.register(r'semesters', SemesterViewSet, basename='semester')
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', summary, name='summary'),
]