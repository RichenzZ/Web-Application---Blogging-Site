"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
import intro.views
import course.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('intro/hello-world', intro.views.hello_world_simple),
    path('intro/hello.html', intro.views.hello),
    path('intro/hello-world-2', intro.views.hello_world_template),
    path('course/course.html', course.views.create_student),

]
