from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=150)
    exams_taken = models.ForeignKey("ExamMaker.Test", related_name="students_taken", on_delete=models.PROTECT, null=True)


class Subject(models.Model):
    name = models.CharField(max_length=50)
    period = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(User, related_name="subjects", on_delete=models.CASCADE)
    students = models.ForeignKey(Student, related_name="students_enrolled_in_subject", on_delete=models.PROTECT, null=True)
    exams = models.ForeignKey("ExamMaker.Test", related_name="exams_made_for_subject", on_delete=models.PROTECT, null=True)
