import shutil
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=20)
    number_of_questions = models.SmallIntegerField(validators=[MinValueValidator(1)])
    number_of_choices = models.SmallIntegerField(validators=[MinValueValidator(3), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    directory = models.TextField(blank=True)

    def delete(self):
        try:
            shutil.rmtree(self.directory)
        except FileNotFoundError:
            pass
        super().delete()
