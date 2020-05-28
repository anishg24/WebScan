from django.http import HttpResponse, FileResponse, Http404, QueryDict
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.views.generic.edit import BaseUpdateView
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ExamSerializer


from .models import Test
from .forms import TestForm
from .exam import Exam

# class TodoView(viewsets.ModelViewSet):
#     serializer_class = ExamSerializer
#     queryset = Test.objects.all()

class TestListView(ListView):
    model = Test
    context_object_name = "tests"
    paginate_by = 10
    queryset = Test.objects.get_queryset().order_by("edited_at")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_exam"] = "active"
        context["header"] = "Exams"
        return context


class TestCreateView(CreateView):
    model = Test
    fields = ("name", "number_of_questions", "number_of_choices")
    success_url = reverse_lazy("exam_list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_exam"] = "active"
        context["header"] = "Exams"
        return context


class TestEditView(UpdateView):
    model = Test
    fields = ("name", "number_of_questions", "number_of_choices")
    template_name = "ExamMaker/test_edit_form.html"
    success_url = reverse_lazy("exam_list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_exam"] = "active"
        context["header"] = "Exams"
        return context

    # def post(self, request, *args, **kwargs):
    #     object = self.get_object()
    #     print(object.name)
    #     return super(BaseUpdateView, self).post(request, *args, **kwargs)


class TestDeleteView(DeleteView):
    model = Test
    success_url = reverse_lazy("exam_list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_exam"] = "active"
        context["header"] = "Exams"
        return context


def print_exam(request, pk):
    test = Test.objects.get(pk=pk)
    exam = Exam(pk, test.name, test.number_of_questions, test.number_of_choices)
    exam.save_pdf()
    directory = exam.get_directory()
    test.directory = directory
    try:
        return FileResponse(open(f"{directory}/paper.pdf", "rb"), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()
