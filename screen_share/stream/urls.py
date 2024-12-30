from django.urls import path
from . import views

urlpatterns = [
    path('', views.screen_share, name='screen_share'),
    path('start-server/', views.start_streaming_server, name='start_server'),
    path('start-client/', views.start_screen_sharing, name='start_client'),
]
