from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.db import transaction
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.core import serializers


from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from mimetypes import guess_type

from grumblr.models import *
from grumblr.forms import *


@ensure_csrf_cookie  # Gives CSRF token for later requests.
@login_required
def home(request):
    items = Item.objects.all().order_by('-date')
    entries = Entry.objects.filter(owner=request.user).first()
    return render(request, 'global.html', {"items": items, "user": request.user, 'entries':entries})
	# return render(request, 'global.html', {})

@login_required
def follower_stream(request):
	followings = Person.objects.get(user=request.user).get_follow()
	items = Item.objects.none()
	for following in followings:
		items = items | Item.objects.filter(user=following.user)
	items = items.order_by('-date')
	entries = Entry.objects.filter(owner=request.user).first()
	return render(request, 'followers.html', {'items': items, "user": request.user,'entries':entries})

@login_required
def follow(request, user_id):
	if user_id != request.user.id:
		user = User.objects.get(id=user_id)
		from_person = Person.objects.get(user=request.user)
		to_person = Person.objects.get(user=user)
		relationship = Relationship.add_follow(from_person, to_person)
		relationship.save()
	return redirect(reverse('follower_stream'))

@login_required
def unfollow(request, user_id):
	if user_id != request.user.id:
		user = User.objects.get(id=user_id)
		from_person = Person.objects.get(user=request.user)
		to_person = Person.objects.get(user=user)
		Relationship.remove_follow(from_person, to_person)
	return redirect(reverse('follower_stream'))

@login_required
def profile(request):
	user = request.user
	items = Item.objects.filter(user=user).order_by('-date')
	entries = Entry.objects.filter(owner=user).first()
	status = True
	return render(request, 'profile.html', {'items': items, "user":user, 'entries':entries, 'status':status})

@login_required
def view_profile(request, user_id=None):
	if not user_id:
		user_id = request.user.id
	user = User.objects.get(id=user_id)
	from_person = Person.objects.get(user=request.user)
	to_person = Person.objects.get(user=user)
	status = False
	if from_person and to_person:
		relationship = Relationship.objects.filter(from_person=from_person, to_person=to_person)
		if relationship or user == request.user:
			status = True
	items = Item.objects.filter(user=user).order_by('-date')
	entries = Entry.objects.filter(owner=user).first()
	return render(request, 'profile.html', {'items': items, "user":user, 'entries':entries, 'status':status})

@login_required
@transaction.atomic
def add_post(request):
	message = []
	item = request.POST.get('item')
	if not item:
		message = "oops, you need to enter something"
	else:
		new_item = Item(text=item, user=request.user)
		new_item.save()
	items = Item.objects.all().order_by('-date')
	entries = Entry.objects.filter(owner=request.user).first()
	context = {'items': items, 'message': message, 'entries':entries}
	return render(request, 'global.html', context)

# def update_post(request):
	

@login_required
@transaction.atomic
def add_comment(request, pk):
	post = Item.objects.get(pk=pk)
	text = request.POST.get('comment')
	if text:
		new_comment = Comment(user=request.user, post=post, text=text)
		new_comment.save()
	items = Item.objects.all().order_by('-date')
	entries = Entry.objects.filter(owner=request.user).first()
	context = {'items': items, 'entries': entries, "max_time": max_time}
	return render(request, 'global.html', context)

@login_required
def add_entry(request):
	context = {}
	my_entry = Entry.get_entries(request.user)
	if not my_entry:
		my_entry = Entry(owner=request.user)
	if request.method == 'GET':
		context['form'] = EntryForm(instance=my_entry)
		context['user'] = request.user
		return render(request, 'editprofile.html', context)

	form = EntryForm(request.POST, request.FILES, instance=my_entry)	
	context['form'] = form	
	if not form.is_valid():
		return render(request, 'editprofile.html', context)
	form.save()
	return redirect(reverse('profile'))

@login_required
def get_photo(request, user_id):
	user = User.objects.get(id=user_id)
	entry = get_object_or_404(Entry, owner=user)
	if not entry.picture:
		raise Http404
	content_type = guess_type(entry.picture.name)
	return HttpResponse(entry.picture, content_type=content_type)

@transaction.atomic
def sign_up(request):
	context = {}
	if request.method == 'GET':
		context['form'] = RegistrationForm()
		return render(request, 'signup.html', context)
	form = RegistrationForm(request.POST)
	context['form'] = form
	if not form.is_valid():
		return render(request, 'signup.html', context)
	new_user = User.objects.create_user(username=form.cleaned_data['username'],
										email=form.cleaned_data['email'],
                                        password=form.cleaned_data['password1'],)
	new_user.first_name = form.cleaned_data['firstname']
	new_user.last_name = form.cleaned_data['lastname']
	new_user.is_active = False
	new_user.save()
	person = Person(user=new_user)
	person.save()
	token = default_token_generator.make_token(new_user)
	email_body = """this is a link to confirm your email
		http://%s%s
		""" % (request.get_host(),
			reverse('email_confirm', args=(new_user.username, token)))
	send_mail(subject='confirm email', 
					message=email_body,	
					from_email='zhaoc2@cmu.edu', 
					recipient_list=[new_user.email])
	context['email'] = form.cleaned_data['email']
	return render(request, 'email_confirm.html', context)

def email_confirm(request, username, token):
	if token and username:
		user = User.objects.get(username=username)
		if default_token_generator.check_token(user, token):
			user.is_active = True
			user.save()
			login(request, user)
			return redirect(reverse('home'))
		user.delete()
	return redirect(reverse('signup'))

@login_required
def reset_password(request):
	context = {}
	user = request.user
	token = default_token_generator.make_token(user)
	email_body = """this is a link to change your password
		http://%s%s
		""" % (request.get_host(),
			reverse('password_confirm', args=(user.username, token)))
	send_mail(subject='reset password', 
					message=email_body,	
					from_email='zhaoc2@cmu.edu', 
					recipient_list=[user.email])
	context['email'] = user.email
	return render(request, 'password_confirm.html', context)

def password_confirm(request, username, token):
	if token and username:
		user = User.objects.get(username=username)
		if default_token_generator.check_token(user, token):
			return redirect(reverse('password_change'))
	return redirect(reverse('login'))

def password_change(request):
	context = {}
	if request.method == 'GET':
		return render(request, 'change_password.html', context)
	if request.POST:
		username = request.POST.get('username')
		new_password = request.POST.get('password')
		if not new_password:
			return render(request, 'change_password.html', context)
		user = User.objects.get(username=username)
		user.set_password(new_password)
		user.save()
	return redirect(reverse('login'))

def forget_password(request):
	context = {}
	if request.method == 'GET':
		return render(request, 'forget_password.html', context)
	username = request.POST.get('username')
	email = request.POST.get('email')
	user = User.objects.get(username=username)
	if user.email == email:
		token = default_token_generator.make_token(user)
		email_body = """this is a link to change a password
			http://%s%s
			""" % (request.get_host(),
				reverse('password_confirm', args=(user.username, token)))
		send_mail(subject='reset password', 
						message=email_body,	
						from_email='zhaoc2@cmu.edu', 
						recipient_list=[user.email])
		context['email'] = user.email
		return render(request, 'password_confirm.html', context)
	print('username or email is wrong!')
	return render(request, 'forget_password.html', context)

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
	raise forms.ValidationError("Username or Password is wrong")
	return render(request, 'login.html', context)

@login_required
def log_out(request):
	logout(request)
	return redirect(reverse('login'))

# Returns all recent additions in the database, as JSON
def get_items(request, time="1970-01-01T00:00+00:00"):
    max_time = Item.get_max_time()
    print(max_time, time)
    items = Item.get_items(time)
    context = {"max_time": max_time, "items": items}
    return render(request, 'posts.json', context, content_type='application/json')


# Returns all recent changes to the database, as JSON
def get_changes(request, time="1970-01-01T00:00+00:00"):
	max_time = Item.get_max_time()
	try:
		items = Item.get_changes(time)
	except:
		time = "1970-01-01T00:00+00:00"
		items = Item.get_changes(time)
	context = {"max_time": max_time, "items": items}
	return render(request, 'posts.json', context, content_type='application/json')


def add_item(request):
    if not 'item' in request.POST or not request.POST['item']:
        raise Http404
    else:
        new_item = Item(text=request.POST['item'], user=request.user)
        new_item.save()
    return HttpResponse("")  # Empty response on success.


def update_comment(request):
	context = {}
	if not 'comment' in request.POST or not request.POST['comment']:
		raise Http404
		# print('no comment')
		# return HttpResponse("")  # Empty response on success.
	else:
		item_pk = request.POST['item-pk']
		post = Item.objects.get(pk=item_pk)
		new_comment = Comment(user=request.user, post=post, text=request.POST['comment'])
		new_comment.save()
		context = {"item_pk": item_pk, "comment_html": new_comment.html}
	return render(request, 'comment.json', context, content_type='application/json')

