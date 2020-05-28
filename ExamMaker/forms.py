from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Test


# Obsolete
class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ("name", "number_of_questions", "number_of_choices")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save Test"))
