"""paper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from paperQ.views import *

urlpatterns = [
    path('/', startpage),
    path('admin/', admin.site.urls),
    path('user_main/', startpage),
    path('register_person/', register_person),
    path('answerpage/<slug:person_name>/<slug:groupname>/<int:index>/', start_answer),
    path('register_answer/<slug:person_name>/<slug:groupname>/<int:index>/', register_answer),
    path('finishpage/', finishpage),
    path('answercheck/<slug:person_name>/<slug:question_group>/',answer_check),
    path('uploadpage/', show_upload),
    path('register_qgroup/', upload),
]
