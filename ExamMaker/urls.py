from django.urls import path
from .views import TestListView, TestCreateView, TestEditView, TestDeleteView, print_exam
urlpatterns = [
    path("", TestListView.as_view(), name="exam_list"),
    path("create/", TestCreateView.as_view(), name="create_exam"),
    path("<int:pk>/edit/", TestEditView.as_view(), name="edit_exam"),
    path("<int:pk>/delete/", TestDeleteView.as_view(), name="delete_exam"),
    path("<int:pk>/print/", print_exam, name="print_exam")
]