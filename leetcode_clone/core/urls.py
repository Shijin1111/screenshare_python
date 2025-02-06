# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.problem_list, name='problem_list'),
    path('problem_detail/<int:problem_id>/', views.problem_detail, name='problem_detail'),
]
