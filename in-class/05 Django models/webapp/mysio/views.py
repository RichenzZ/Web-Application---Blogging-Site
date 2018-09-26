from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from mysio.models import *


# Create your views here.
def home(request):
    return render(request, 'sio.html', {})

def add_student(request):
    errors = []  # A list to record messages for any errors we encounter.

    # Adds the new item to the database if the request parameter is present
    if not 'andrew-id' in request.POST or not request.POST['andrew-id']:
        errors.append('You must enter an student to add.')
    else:
        new_item = student(andrewid = request.POST['andrew-id'],firstname = request.POST['first-name'],lastname = request.POST['last-name'])
        new_item.save()

    # Sets up data needed to generate the view, and generates the view
    items = student.objects.all()
    context = {'student':items, 'errors':errors}
    return render(request, 'sio/index.html', context)

def add_course(request):
    errors = []  # A list to record messages for any errors we encounter.

    # Adds the new item to the database if the request parameter is present
    if not 'course-number' in request.POST or not request.POST['course-number']:
        errors.append('You must enter an course to add.')
    else:
        new_item = student(coursenum = request.POST['course-number'],coursename = request.POST['course-name'], courseins = request.POST['instructor'])
        new_item.save()

    # Sets up data needed to generate the view, and generates the view
    items = course.objects.all()
    context = {'course':items, 'errors':errors}
    return render(request, 'sio/index.html', context)
