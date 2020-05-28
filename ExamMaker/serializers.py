from rest_framework import serializers
from .models import Exam

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ("name", "number_of_questions", "number_of_choices", "created_at", "edited_at", "directory")