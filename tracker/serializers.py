from rest_framework import serializers
from .models import Semester, Course, GRADE_POINTS
from decimal import Decimal

class CourseSerializer(serializers.ModelSerializer):
    grade_point = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'semester', 'code', 'title', 'unit', 'grade', 'grade_point']
        read_only_fields = ['grade_point']

    def get_grade_point(self, obj):
        return str(GRADE_POINTS.get(obj.grade or 'F', Decimal('0')))

class SemesterSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    total_units = serializers.SerializerMethodField()
    gpa = serializers.SerializerMethodField()

    class Meta:
        model = Semester
        fields = ['id', 'name', 'level', 'start_date', 'end_date', 'created_at',
                  'total_units', 'gpa', 'courses']

    def get_total_units(self, obj):
        return obj.total_units()

    def get_gpa(self, obj):
        # return as string to keep consistent decimal formatting
        return str(obj.gpa())