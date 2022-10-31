from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#Form will be used to authenticate users against the database.

class LoginForm(forms.Form):

    username = forms.CharField()

    # widget will render password HTML
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
           model = User
           fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

from .models import Profile
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 
					'last_name', 
					'email')


class ProfileEditForm(forms.ModelForm):
	BIRTH_YEAR_CHOICES = list(str(year) for year in list(range(1940,2004)))
	date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    
	class Meta:
		model = Profile
		fields = ('date_of_birth',
					'occupation',
					'about_me',
					 'photo',
					  'proposal_time',
					  'proposal_location')
