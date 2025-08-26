from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

GRADE_POINTS = {
    'A': Decimal('5.0'),
    'B': Decimal('4.0'),
    'C': Decimal('3.0'),
    'D': Decimal('2.0'),
    'E': Decimal('1.0'),
    'F': Decimal('0.0'),
}

class Semester(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='semesters')
    name = models.CharField(max_length=100)  # e.g. "2024/2025 - First"
    level = models.CharField(max_length=50, blank=True)  # e.g. "300L"
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_units(self):
        return sum(c.unit for c in self.courses.all())

    def total_weighted_points(self):
        total = Decimal('0')
        for c in self.courses.all():
            gp = GRADE_POINTS.get(c.grade or 'F', Decimal('0'))
            total += gp * Decimal(c.unit)
        return total

    def gpa(self):
        units = self.total_units()
        return (self.total_weighted_points() / Decimal(units)) if units else Decimal('0')

    def __str__(self):
        return f"{self.name} ({self.owner.username})"

class Course(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='courses')
    code = models.CharField(max_length=20)       # e.g. "MTH101"
    title = models.CharField(max_length=200)
    unit = models.PositiveSmallIntegerField()
    grade = models.CharField(max_length=1, choices=[(g, g) for g in "ABCDEF"], blank=True)

    def __str__(self):
        return f"{self.code} - {self.title}"