# tracker/views_csv.py
import csv, io
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Course, Semester

class CoursesExportCSV(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        semester_id = request.query_params.get("semester")
        qs = Course.objects.filter(semester__user=request.user)
        if semester_id:
            qs = qs.filter(semester_id=semester_id)

        resp = HttpResponse(content_type="text/csv")
        resp['Content-Disposition'] = 'attachment; filename="courses.csv"'
        writer = csv.writer(resp)
        writer.writerow(["id","semester_id","code","title","unit","grade"])
        for c in qs:
            writer.writerow([c.id, c.semester_id, c.code, c.title, c.unit, c.grade])
        return resp

class CoursesImportCSV(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Expect a file in form-data with key 'file'.
        CSV headers: semester_id,code,title,unit,grade
        """
        f = request.FILES.get("file")
        if not f:
            return Response({"detail": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        data = io.TextIOWrapper(f.file, encoding="utf-8")
        reader = csv.DictReader(data)
        created = 0
        for row in reader:
            try:
                sem = Semester.objects.get(id=row["semester_id"], user=request.user)
            except Semester.DoesNotExist:
                continue
            Course.objects.create(
                semester=sem,
                code=row["code"],
                title=row["title"],
                unit=int(row["unit"]),
                grade=row["grade"].strip().upper(),
            )
            created += 1
        return Response({"imported": created}, status=status.HTTP_201_CREATED)