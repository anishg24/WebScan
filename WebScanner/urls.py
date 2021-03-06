"""WebScanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from ExamMaker import views as exam_views
from Classroom import views as class_views
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()
router.register(r"exams", exam_views.TestView, "exam")
router.register(r"subject", class_views.SubjectView, "subject")
router.register(r"student", class_views.StudentView, "student")

schema_view = get_schema_view(
    openapi.Info(
        title="MyAPI",
        default_version="v1",
        description="Test Description",
        contact=openapi.Contact(email="anishg24@gmail.com")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    url(r"^", schema_view.with_ui("swagger"), name="schema-swagger-ui"),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
