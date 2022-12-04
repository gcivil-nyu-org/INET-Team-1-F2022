from .models import Profile,newLocation, Match_Feedback
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.safestring import mark_safe
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
    # proposal_date_new = forms.DateField(widget=forms.SelectDateWidget(attrs={'type': 'date'}))
    # proposal_time_new = forms.TimeField()
    proposal_datetime_local = forms.CharField(widget=forms.TextInput(attrs={'type':'datetime-local'}))
    class Meta:
        model = Profile
        fields = ('date_of_birth',
                  'occupation',
                  'about_me',
                  'gender_identity',
                  'sexual_orientation',
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
                  'gender_preference',
                  'orientation_preference')




class MatchFeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.label_suffix = ""  # Removes : as label suffix
    DATE_HAPPENED_CHOICES = (('Yes', ' We both showed up'), ('No1', ' My match wasn’t there'), ('No2', 'I didn’t go'))
#     N/A
# Sexual harrasment
# Person didn’t match the profile
# Rude / Unfriendly
# Made me feel uncomfortable

    BEHAVIOR_CHOICES = (('N/A', ' None'),
                         ('Uncomfortable', ' Made me feel uncomfortable'), 
                         ('Rude', ' Rude / Unfriendly'),
                         ('Catfish',' Person didn’t match the profile'),
                         ('Advances',  'Made inappropriate advances'),
                         ('Harrassment', ' Report Harrassment'),
                         ('Other',' Other')
                         )
    RATING_CHOICES = [(x,x) for x in range(0,11)]
    date_happened = forms.ChoiceField(label=mark_safe('<strong>Did the date take place?</strong>'),
                                widget=forms.RadioSelect(attrs={'class': 'checkbox'}),
                                 choices=DATE_HAPPENED_CHOICES,
                                 )
    match_rating = forms.ChoiceField(label=mark_safe("<p><strong>Please rate your match on a scale from 0 (bad) to 10 (perfect): </br> </strong> </p>"),
                                choices=RATING_CHOICES)
    inappropriate_behavior = forms.ChoiceField(label=mark_safe("<strong>Report inappropriate behavior</strong>"),
                                widget=forms.RadioSelect(attrs={'label':'Name','class': 'checkbox'}),
                                 choices=BEHAVIOR_CHOICES)

    match_comments = forms.CharField(label=mark_safe("<strong>Please use this section to provide any personal comments on how the date went. <br> (If you didn't attend, or the match behaved inappropriately, please provide additional details): </strong> "),
                                widget=forms.Textarea(attrs={'class': 'textarea rows="8"'}))
    class Meta:
        model = Match_Feedback
        fields = ('date_happened',
                'match_rating',
                'inappropriate_behavior',
                'match_comments',)     

