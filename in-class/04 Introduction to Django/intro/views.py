from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def hello_world_simple(request):
	response_string = """
	<!DOCTYPE HTML>
	<html>
	<head>
	 <meta charset="utf-8">
	 <title> Hello World</title>
	</head>

	<body>
	<h1>Hello, world!</h1>
	</body>
	</html>

	"""
	return HttpResponse(response_string)

def  hello_world_template(request):
	return render(request, 'generic-hello.html-template', {})

def hello(request):
	context = {}
	context['person_name'] = ''

	if 'username' in request.GET:
		context['person_name'] = request.GET['username']

	return render(request, 'greet.html', context)