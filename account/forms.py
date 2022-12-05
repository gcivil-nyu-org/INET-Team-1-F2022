from .models import Profile,newLocation
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
import datetime


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

    years_list = [ i for i in range(1900, 2022) ]

    date_of_birth = forms.DateField(
        widget = forms.SelectDateWidget(
            years = years_list,
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
        ),
    )

    def is_adult(self):
        dob = self.cleaned_data['date_of_birth']
        if (datetime.date.today() - dob  ) > datetime.timedelta(days=18*365):
            return True
        return False

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'date_of_birth')

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
    def check_username(self):
        username = self.cleaned_data.get('first_name')
        undefined = ('@', '.', '-', '+')
        print(username)
        if username == "":
            self.add_error('first_name','First Name cannot be empty!')
            # raise forms.ValidationError('Username cannot be empty!')
        if any([char in username for char in undefined]):
            self.add_error('first_name','Symbols @/./-/+ are not allowed in username.')
            # raise forms.ValidationError('Symbols @/./-/+ are not allowed in username.')
        return username

class ProfileEditForm(forms.ModelForm):
    BIRTH_YEAR_CHOICES = list(str(year) for year in list(range(1940, 2004)))
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    about_me = forms.CharField(widget=forms.Textarea)
    #proposal_time = forms.DateTimeField(widget=forms.DateTimeInput)
    # proposal_date_new = forms.DateField(widget=forms.SelectDateWidget(attrs={'type': 'date'}))
    # proposal_time_new = forms.TimeField()
    proposal_datetime_local = forms.CharField(widget=forms.TextInput(attrs={'type':'datetime-local'}))
    class Meta:
        model = Profile
        fields = ('date_of_birth',
                  'occupation',
                  'about_me',
                  'gender_identity',
                #   'sexual_orientation',
                  'photo',
                  'proposal_datetime_local'
                  )
        # widgets = {
        #     'proposal_date_new': forms.SelectDateWidget(attrs={'type': 'date'}),
        #     'proposal_time_new': forms.TimeInput(attrs={'type': 'time'})
        # }

class NewLocationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('cusine',
                    'boro',
                    'location_dropdown')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location_dropdown'].queryset = newLocation.objects.all()

        if 'cusine' and 'boro' in self.data:
            try:
                cusine_id = int(self.data.get('cusine'))
                boro_id = int(self.data.get('boro'))
                self.fields['location_dropdown'].queryset = newLocation.objects.filter(CUISINE_id=cusine_id,BORO_id = boro_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['city'].queryset = self.instance.country.city_set.order_by('name')

class PreferenceEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('age_preference_min',
                  'age_preference_max',
                  'gender_preference')
