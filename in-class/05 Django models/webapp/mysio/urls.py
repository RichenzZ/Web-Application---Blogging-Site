from django.urls import path
import mysio.views

urlpatterns = [
    path('', mysio.views.home),
    path('add-student', mysio.views.add_student),
    path('add-course', mysio.views.add_course),
]
