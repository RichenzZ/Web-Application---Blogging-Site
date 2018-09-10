from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def create_student(request):
	context = {}
	context['andrewid'] = ''
	context['fisrtname'] = ''
	context['lastname'] = ''

	if 'andrewid' in request.GET:
		context['andrewid'] = request.GET['andrewid']
	if 'andrewid' in request.GET:
		context['fisrtname'] = request.GET['lastname']
	if 'lastname' in request.GET:
		context['lastname'] = request.GET['lastname']
	return render(request, 'reg.html', context)

