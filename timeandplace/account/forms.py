from .models import Profile,newLocation
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Form will be used to authenticate users against the database.

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


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'email')


class ProfileEditForm(forms.ModelForm):
    BIRTH_YEAR_CHOICES = list(str(year) for year in list(range(1940, 2004)))
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    about_me = forms.CharField(widget=forms.Textarea)
    #proposal_time = forms.DateTimeField(widget=forms.DateTimeInput)
    class Meta:
        model = Profile
        fields = ('date_of_birth',
                  'occupation',
                  'about_me',
                  'gender_identity',
                  'sexual_orientation',
                  'photo',
                  'proposal_time',
                  'location_drawdown')
                # 'age')
                #   'age_preference_min',
                #   'age_preference_max',
                #   'gender_preference',
                #   'orientation_preference')

class NewLocationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('cusine',
                  'location_dropdown')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location_dropdown'].queryset = newLocation.objects.none()

        if 'cusine' in self.data:
            try:
                cusine_id = int(self.data.get('cusine'))
                self.fields['location_dropdown'].queryset = newLocation.objects.filter(CUISINE_id=cusine_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

class PreferenceEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('age_preference_min',
                  'age_preference_max',
                  'gender_preference',
                  'orientation_preference')
