from rest_framework import viewsets
from .serializers import ExamSerializer

from .models import Test
from .exam import Exam


class TestView(viewsets.ModelViewSet):
    serializer_class = ExamSerializer
    queryset = Test.objects.all()
