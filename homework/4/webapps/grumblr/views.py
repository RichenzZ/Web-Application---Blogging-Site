from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.db import transaction
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from mimetypes import guess_type

from grumblr.models import *
from grumblr.forms import *

# Create your views here.
@login_required
def home(request):
    items = Item.objects.all().order_by('-date')
    entries = Entry.objects.filter(owner=request.user).first()
    return render(request, 'global.html', {'items': items, "user": request.user, 'entries':entries})

@login_required
def follower_stream(request):
	followings = Person(user=request.user).get_follow() #person object
	users = followings.user
	items = Item.objects.none()
	for following in followings:
		items = items | Item.objects.filter(user=following.user)
	items = items.order_by('-date')
	return render(request, 'global.html', {'items': items, "user": request.user})

@login_required
def follow(request, user_id):
	if user_id != request.user.id:
		user = User.objects.get(id=user_id)
		from_person = Person.objects.get(user=request.user)
		to_person = Person.objects.get(user=user)
		relationship = Relationship.add_follow(from_person, to_person)
		relationship.save()
	return redirect(reverse('profile'))

@login_required
def unfollow(request, user_id):
	if user_id != request.user.id:
		user = User.objects.get(id=user_id)
		from_person = Person.objects.get(user=request.user)
		to_person = Person.objects.get(user=user)
		Relationship.remove_follow(from_person, to_person)
	return redirect(reverse('profile'))

@login_required
def profile(request):
    items = Item.objects.filter(user=request.user).order_by('-date')
    # entries = Entry.get_entries(request.user)
    entries = Entry.objects.filter(owner=request.user).first()
    # print(entries)
    return render(request, 'profile.html', {'items': items, "user":request.user, 'entries':entries})

@login_required
def view_profile(request, user_id):
	user = User.objects.get(id=user_id)
	items = Item.objects.filter(user=user).order_by('-date')
	# entries = Entry.get_entries(user)
	entries = Entry.objects.filter(owner=user)
	return render(request, 'profile.html', {'items': items, "user":user, 'entries':entries})

@login_required
@transaction.atomic
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

@login_required
def add_entry(request):
	# def add_e():
	context = {}
	my_entry = Entry.get_entries(request.user)
	if request.method == 'GET':
		context['form'] = EntryForm(instance=my_entry)
		return render(request, 'editprofile.html', context)

	form = EntryForm(request.POST, request.FILES, instance=my_entry)	
	# form = EntryForm(request.POST)	
	context['form'] = form	
	if not form.is_valid():
		return render(request, 'editprofile.html', context)
	form.save()
	return redirect(reverse('profile'))
	# return render(request, 'editprofile.html', context)
	# transaction.on_commit(add_e)

@login_required
def edit_entry(request):
	# def edit_e():
	# entry_to_edit = get_object_or_404(Entry, owner=request.user)
	# entry_to_edit = Entry.objects.filter(owner=request.user)
	# entry_to_edit = Entry.objects.get(owner=request.user)
	entry_to_edit = Entry.get_entries(request.user)
	if request.method == 'GET':
		form = EntryForm(instance=entry_to_edit)
		context = {'form':form}
		return render(request, 'editprofile.html', context)
	form = EntryForm(request.POST, instance=entry_to_edit)		
	if not form.is_valid():
		context = {'form':form}
		return render(request, 'editprofile.html', context)
	form.save()
	return redirect('profile/')
	# transaction.on_commit(edit_e)

@login_required
def get_photo(request):
	# entry = get_object_or_404(Entry, owner=request.user)
	# if not entry.picture:
	# 	raise Http404
	entry = Entry.get_entries(request.user)
	if not entry.picture:
		print('no photo!')
		return redirect(reverse('profile'))
	content_type = guess_type(entry.picture.name)
	return HttpResponse(entry.picture, content_type=content_type)

@transaction.atomic
def sign_up(request):
	context = {}
	# display the sign up form if it is a get request
	if request.method == 'GET':
		context['form'] = RegistrationForm()
		return render(request, 'signup.html', context)
	form = RegistrationForm(request.POST)
	context['form'] = form
	if not form.is_valid():
		return render(request, 'signup.html', context)
	new_user = User.objects.create_user(username=form.cleaned_data['username'],
										email=form.cleaned_data['email1'],
								    	firstname=form.cleaned_data['firstname'],
								    	lastname=form.cleaned_data['lastname'],
                                        password=form.cleaned_data['password1'])

	new_user.save()
	login(request, new_user)
	return redirect(reverse('home'))
    # Logs in the new user and redirects to his/her todo list
    # new_user = authenticate(username=form.cleaned_data['username'], \
    #                         password=form.cleaned_data['password1'])


def log_in(request):
	context = {}
	if request.method == 'GET':
		context['form'] = RegistrationForm()
		return render(request, 'login.html', context)
	form = RegistrationForm(request.POST)
	user = authenticate(username=form.cleaned_data['username'],
                        password=form.cleaned_data['password1'])
	if user is not None:
		login(request, user)
		return redirect('/global/') # done by settings.LOGIN_REDIRECT_URL
		# return render(request, 'global.html', {"user":user})
	raise forms.ValidationError("Username or Password is wrong")
	return render(request, 'login.html', context)

@login_required
def log_out(request):
	logout(request)
	# redirect to another page
	# return render(request, 'login.html')
	return redirect(reverse('login'))

@login_required
def reset_password(request):
	context = {}
	email_body = 'this is a link to reset your password'
	send_mail(subject='reset password', message=email_body,	from_email='zhaochen@cmu.edu', recipient_list=[request.user.email])	
	context['email'] = form.cleaned_data['email1']
	return render(request, 'global.html', context)

