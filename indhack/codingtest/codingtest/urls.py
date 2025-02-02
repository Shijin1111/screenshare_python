"""
URL configuration for codingtest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from testsystem.views import coding_test, submit_code,home
from compiler.views import run_code

urlpatterns = [
    path('admin/', admin.site.urls),
    path('compiler/', include('compiler.urls')),
    path('', home, name='home'), 
    path('test/<int:question_id>/', coding_test, name='coding_test'),
    path('testsystem/submit/<int:question_id>/', submit_code, name='submit_code'),
    path('compiler/run_code/', run_code, name='run_code'),
]
