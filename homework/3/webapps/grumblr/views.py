from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from grumblr.models import *

# Create your views here.
@login_required
def home(request):
    items = Item.objects.all().order_by('-date')
    return render(request, 'global.html', {'items': items, "user": request.user})

@login_required
def profile(request):
    items = Item.objects.filter(user=request.user).order_by('-date')
    return render(request, 'profile.html', {'items': items, "user":request.user})

@login_required
def view_profile(request, user_id):
	user = User.objects.get(id=user_id)
	items = Item.objects.filter(user=user).order_by('-date')
	return render(request, 'profile.html', {'items': items, "user":user})

@login_required
def add_post(request):
	message = []
	# check errors
	# ............
	item = request.POST.get('item')
	if not item:
		message = "oops, you need to enter something"
	else:
		new_item = Item(text=item, user=request.user)
		new_item.save()
	items = Item.objects.all().order_by('-date')
	context = {'items': items, 'message': message}
	return render(request, 'global.html', context)



def sign_up(request):
	context = {}
	# display the sign up form if it is a get request
	if request.method == 'GET':
		return render(request, 'signup.html', context)
	messages = []
	username = request.POST.get('username')
	password = request.POST.get('password')
	confirmpassword = request.POST.get('confirmpassword')
	email = request.POST.get('email')
	firstname = request.POST.get('firstname')
	lastname = request.POST.get('lastname')
	# need check errors
	# .................
	if email:
		context["email"] = email
	if not username:
		messages.append("username is required")
	else:
		context["username"] = username
	if not firstname:
		messages.append("firstname is required")
	else:	
		context["firstname"] = firstname
	if not lastname:
		messages.append("lastname is required")
	else:
		context["lastname"] = lastname
	if not password or not confirmpassword:
		messages.append("password is required")
	if password and confirmpassword and password != confirmpassword:
		messages.append('password not match')
	if username and len(User.objects.filter(username=username)):
		messages.append('username is already taken')
	if messages:
		context["messages"] = messages
		return render(request, 'signup.html', context)
	
	if username and password and confirmpassword and lastname and firstname and password == confirmpassword:
		new_user = User.objects.create_user(
		    username=username, email=email, password=password, first_name=firstname, last_name=lastname)
		# need new_user.save() ?
		# need authentication?
		login(request, new_user)
		return redirect('/global/')

	return render(request, 'signup.html', context)


def log_in(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	if username and password:
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('/global/') # done by settings.LOGIN_REDIRECT_URL
			# return render(request, 'global.html', {"user":user})
	# context = {}
	# context["errors"] = 
	return render(request, 'login.html', {"message":"username or password is wrong"})

@login_required
def log_out(request):
	logout(request)
	# redirect to another page
	# return render(request, 'login.html')
	return redirect('../')
