
from django.urls import path
from . import views
from pages.dash_apps.finished_apps import simpleexample

urlpatterns = [
    path('', base_view, name='base_view')
]