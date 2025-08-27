from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SemesterViewSet, CourseViewSet, summary 
from . import views
from .views_csv import CoursesExportCSV, CoursesImportCSV

router = DefaultRouter()
router.register(r'semesters', SemesterViewSet, basename='semester')
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', summary, name='summary'),
    path("courses/export/", CoursesExportCSV.as_view(), name="courses-export"),
    path("courses/import/", CoursesImportCSV.as_view(), name="courses-import"),
]