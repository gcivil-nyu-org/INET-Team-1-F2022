from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class ProfileForm(forms.Form):

	PLACE_CHOICES = (
		(1, 'Coffee shops'),
		(2, 'Bars'),
		(3, 'Restaurants'),
		(4, 'Parks')
	)

	name = forms.CharField(
		label = "Name:"
	)
	bio = forms.CharField(
		label = "Tell us a bit about yourself:",
		max_length = 250
	)
	age = forms.IntegerField(
		label = "How old are you? (You must be 18 years old to create a profile):"
	)
	occupation = forms.CharField(
		label = "Do you work? If so, where?"
	)
	
	place = forms.ChoiceField(
		label = "Please pick an ideal place to meetup with someone:",
		choices=PLACE_CHOICES
	)

	time = forms.CharField()