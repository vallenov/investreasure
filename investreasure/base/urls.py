from django.urls import re_path

from . import views


urlpatterns = [
    re_path(r'^index$', views.MOEXBaseView.as_view()),
]
