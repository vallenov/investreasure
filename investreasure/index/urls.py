from django.urls import re_path

from . import views


urlpatterns = [
    re_path(r'^all', views.IndexAllView.as_view()),
]
