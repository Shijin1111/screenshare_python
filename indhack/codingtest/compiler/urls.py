from django.urls import path
from .views import run_code

urlpatterns = [
    path('run_code/', run_code, name='run_code'),
]
