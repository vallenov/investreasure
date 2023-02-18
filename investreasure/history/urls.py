from django.urls import re_path

from . import views


urlpatterns = [
    re_path(r'^\w+$', views.MOEXHistoryView.as_view()),
]
