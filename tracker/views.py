from rest_framework import viewsets, permissions, decorators, filters
from rest_framework.response import Response
from django.db.models import Sum
from decimal import Decimal
from .models import Semester, Course, GRADE_POINTS
from .serializers import SemesterSerializer, CourseSerializer
from django.http import JsonResponse

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Semester):
            return obj.owner == request.user
        if isinstance(obj, Course):
            return obj.semester.owner == request.user
        return False

class SemesterViewSet(viewsets.ModelViewSet):
    serializer_class = SemesterSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'level']
    ordering_fields = ['created_at', 'name']

    def get_queryset(self):
        return Semester.objects.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code', 'title', 'grade']
    ordering_fields = ['code', 'unit']

    def get_queryset(self):
        return Course.objects.filter(semester__owner=self.request.user).order_by('code')

# Aggregated stats (CGPA across all semesters)
@decorators.api_view(['GET'])
def summary(request):
    user = request.user
    courses = Course.objects.filter(semester__owner=user)
    totals = {'units': 0, 'weighted': Decimal('0')}
    for c in courses:
        gp = GRADE_POINTS.get(c.grade or 'F', Decimal('0'))
        totals['units'] += c.unit
        totals['weighted'] += gp * Decimal(c.unit)
    cgpa = (totals['weighted'] / Decimal(totals['units'])) if totals['units'] else Decimal('0')
    return Response({
        'total_units': totals['units'],
        'total_weighted_points': str(totals['weighted']),
        'cgpa': str(cgpa)
    })

def home(request):
    return JsonResponse({"message": "Welcome to Academic Score Tracker API"})