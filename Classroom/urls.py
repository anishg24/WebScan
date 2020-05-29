from django.urls import path
from .views import SubjectListView, SubjectCreateView, signup, TeacherLoginView, StudentListView, StudentCreateView
from django.contrib.auth import views as auth_views
import Classroom.views as views
urlpatterns = [
    path("", SubjectListView.as_view(), name="subject_list"),
    path("create/", SubjectCreateView.as_view(), name="create_subject"),
    path("signup/", signup, name="signup"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("login/", TeacherLoginView.as_view(), name="login"),
    path("students/", StudentListView.as_view(), name="student_list"),
    path("students/create", StudentCreateView.as_view(), name="create_student"),
    # path("<int:pk>/edit/", TestEditView.as_view(), name="edit_exam"),
    # path("<int:pk>/delete/", TestDeleteView.as_view(), name="delete_exam"),
    # path("<int:pk>/print/", print_exam, name="print_exam")
]