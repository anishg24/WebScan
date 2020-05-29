from rest_framework import serializers
from .models import Test

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ("name", "number_of_questions", "number_of_choices", "created_at", "edited_at", "directory")