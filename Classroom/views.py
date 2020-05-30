from .models import Student, Subject
from .serializers import SubjectSerializer, StudentSerializer
from rest_framework import viewsets


class SubjectView(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class StudentView(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()