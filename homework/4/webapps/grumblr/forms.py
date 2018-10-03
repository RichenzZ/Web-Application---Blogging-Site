from django import forms

from django.contrib.auth.models import User
from grumblr.models import *

class RegistrationForm(forms.Form):
    firstname = forms.CharField(max_length = 20,
                                label='First Name')
    lastname = forms.CharField(max_length = 20,
                                label='Last Name')
    username = forms.CharField(max_length = 20,
                                label='Username')
    email1 = forms.CharField(max_length = 20,
                                label='Email')
    email2 = forms.CharField(max_length = 20,
                                label='Confirm Email')
    password1 = forms.CharField(max_length = 200,
                                label='Password',
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200,
                                label='Confirm password',
                                widget = forms.PasswordInput())


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        email1 = cleaned_data.get('email1')
        email2 = cleaned_data.get('email2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        if email1 and email2 and email1 != email2:
            raise forms.ValidationError("Emails did not match.")
        # Generally return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return username

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        exclude = ('owner', )
        widgets = {'picture': forms.FileInput()}
        # fields = ('firstname', 'last_name', ...)


