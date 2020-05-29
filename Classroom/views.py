from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from .forms import SignUpForm
from .models import Student, Subject


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("subject_list")
    else:
        form = SignUpForm()
    return render(request, "Classroom/signup.html", {"form": form, "header": "Classroom", "nav_classroom": "active"})


class TeacherLoginView(LoginView):
    template_name = "Classroom/login.html"

    def get_success_url(self):
        return reverse_lazy("subject_list")


class SubjectListView(ListView):
    model = Subject
    context_object_name = "subjects"
    paginate_by = 10
    queryset = Subject.objects.get_queryset().order_by("period")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_classroom"] = "active"
        context["header"] = "Classroom"
        return context


class SubjectCreateView(CreateView):
    model = Subject
    fields = ("name", "period", "description")
    success_url = reverse_lazy("subject_list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_classroom"] = "active"
        context["header"] = "Classroom"
        return context

    def form_valid(self, form):
        subject = form.save(commit=False)
        subject.teacher = self.request.user
        subject.students = None
        subject.exams = None
        subject.save()
        return super().form_valid(form)


class StudentListView(ListView):
    model = Student
    context_object_name = "students"
    paginate_by = 10
    queryset = Student.objects.get_queryset().order_by("name")
    template_name = "Classroom/student_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_classroom"] = "active"
        context["header"] = "Classroom"
        return context


class StudentCreateView(CreateView):
    model = Student
    fields = ("name",)
    success_url = reverse_lazy("student_list")

    def form_valid(self, form):
        student = form.save(commit=False)
        student.exams_taken = None
        student.save()
        return super().form_valid(form)
