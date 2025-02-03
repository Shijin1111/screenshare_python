from django.urls import path
from .views import execute_code,submit_code,home

urlpatterns = [
    path('', home, name='home'),
    path('execute/', execute_code, name='execute_code'),
    path('submit/<int:question_id>/', submit_code, name='submit_code'),
]
