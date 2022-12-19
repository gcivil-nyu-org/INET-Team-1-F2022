from .models import Profile, newLocation, Match_Feedback
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
import datetime
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from .models import Comment
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

    years_list = [i for i in range(1922, 2023)]

    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(
            years=years_list,
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
        ),
    )

    def is_adult(self):
        dob = self.cleaned_data['date_of_birth']
        if (datetime.date.today() - dob) > datetime.timedelta(days=18*365):
            return True
        return False

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'date_of_birth')

    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError('Passwords don\'t match.')
    #     return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'email')

    def check_username(self):
        username = self.cleaned_data.get('first_name')
        undefined = ('@', '.', '-', '+')
        # print(username)
        if username == "":
            self.add_error('first_name', 'First Name cannot be empty!')
            # raise forms.ValidationError('Username cannot be empty!')
        if any([char in username for char in undefined]):
            self.add_error('first_name', 'Symbols @/./-/+ are not allowed in username.')
            # raise forms.ValidationError('Symbols @/./-/+ are not allowed in username.')
        return username


class ProfileEditForm(forms.ModelForm):
    BIRTH_YEAR_CHOICES = list(str(year) for year in list(range(1940, 2004)))
    # date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    about_me = forms.CharField(widget=forms.Textarea)
    #proposal_time = forms.DateTimeField(widget=forms.DateTimeInput)
    # proposal_date_new = forms.DateField(widget=forms.SelectDateWidget(attrs={'type': 'date'}))
    # proposal_time_new = forms.TimeField()
    # proposal_datetime_local = forms.CharField(
    #     widget=forms.TextInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Profile
        fields = ( #   'date_of_birth',
                  'occupation',
                  'about_me',
                  'gender_identity',
                    #   'sexual_orientation',
                  'photo',
                    #  'proposal_datetime_local'
                  )
        # widgets = {
        #     'proposal_date_new': forms.SelectDateWidget(attrs={'type': 'date'}),
        #     'proposal_time_new': forms.TimeInput(attrs={'type': 'time'})
        # }

class TimeEditForm(forms.ModelForm):
    proposal_datetime_local = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Profile
        fields = ('proposal_datetime_local',)

    def check_time_is_valid(self):
        time_proposal = self.cleaned_data.get('proposal_datetime_local')
        time_now = timezone.now()
        # time_proposal_datetime_obj = parse_datetime(time_proposal)
        if parse_datetime(time_proposal) > time_now:
            return True
        else:
            self.add_error('proposal_datetime_local',
                           "Proposal time must be in the future! Please select another time:")
            return False

class NewLocationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('cusine',
                  'boro',
                  'location_dropdown')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location_dropdown'].queryset = newLocation.objects.none()

        if 'cusine' and 'boro' in self.data:
            try:
                cusine_id = int(self.data.get('cusine'))
                boro_id = int(self.data.get('boro'))
                self.fields['location_dropdown'].queryset = newLocation.objects.filter(
                    CUISINE_id=cusine_id, BORO_id=boro_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.location:
        #     print("im here!")
        #     self.fields['location_dropdown'] = self.location
            # print(self.instance.user.profile.location_dropdown)
            # self.fields['location_dropdown'] = self.instance.location_dropdown

class PreferenceEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('age_preference_min',
                  'age_preference_max',
                  'gender_preference')

    def check_age(self):
        age_preference_MAX = self.cleaned_data.get('age_preference_max')
        age_preference_MIN = self.cleaned_data.get('age_preference_min')
        if age_preference_MAX < age_preference_MIN:
            self.add_error('age_preference_min',
                           "Minimum age has be smaller or equal to the Maximum Age")
            # raise ValidationError("Minimum age has be smaller or equal to the Maximum Age")
            return False
        else:
            return True

class MatchFeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
    DATE_HAPPENED_CHOICES = (('Yes', ' We both showed up'),
                             ('No1', ' My match wasn’t there'), ('No2', 'I didn’t go'))
#     N/A
# Sexual harrasment
# Person didn’t match the profile
# Rude / Unfriendly
# Made me feel uncomfortable

    BEHAVIOR_CHOICES = (('N/A', ' None'),
                        ('Uncomfortable', ' Made me feel uncomfortable'),
                        ('Rude', ' Rude / Unfriendly'),
                        ('Catfish', ' Person didn’t match the profile'),
                        ('Advances',  'Made inappropriate advances'),
                        ('Harrassment', ' Report Harrassment'),
                        ('Other', ' Other')
                        )
    RATING_CHOICES = [(x, x) for x in range(0, 11)]
    date_happened = forms.ChoiceField(label=mark_safe('<strong>Did the date take place?</strong>'),
                                      widget=forms.RadioSelect(attrs={'class': 'checkbox'}),
                                      choices=DATE_HAPPENED_CHOICES,
                                      )
    match_rating = forms.ChoiceField(label=mark_safe("<p><strong>Please rate your match on a scale from 0 (bad) to 10 (perfect): </br> </strong> </p>"),
                                     choices=RATING_CHOICES)
    inappropriate_behavior = forms.ChoiceField(label=mark_safe("<strong>Report inappropriate behavior</strong>"),
                                               widget=forms.RadioSelect(
                                                   attrs={'label': 'Name', 'class': 'checkbox'}),
                                               choices=BEHAVIOR_CHOICES)

    match_comments = forms.CharField(label=mark_safe("<strong>Please use this section to provide any personal comments on how the date went. <br> (If you didn't attend, or the match behaved inappropriately, please provide additional details): </strong> "),
                                     widget=forms.Textarea(attrs={'class': 'textarea rows="8"'}))

    class Meta:
        model = Match_Feedback
        fields = ('date_happened',
                  'match_rating',
                  'inappropriate_behavior',
                  'match_comments',)


class MatchFeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
    DATE_HAPPENED_CHOICES = (('Yes', ' We both showed up'),
                             ('No1', ' My match wasn’t there'), ('No2', 'I didn’t go'))
#     N/A
# Sexual harrasment
# Person didn’t match the profile
# Rude / Unfriendly
# Made me feel uncomfortable

    BEHAVIOR_CHOICES = (('N/A', ' None'),
                        ('Uncomfortable', ' Made me feel uncomfortable'),
                        ('Rude', ' Rude / Unfriendly'),
                        ('Catfish', ' Person didn’t match the profile'),
                        ('Advances',  'Made inappropriate advances'),
                        ('Harrassment', ' Report Harrassment'),
                        ('Other', ' Other')
                        )
    RATING_CHOICES = [(x, x) for x in range(0, 11)]
    date_happened = forms.ChoiceField(label=mark_safe('<strong>Did the date take place?</strong>'),
                                      widget=forms.RadioSelect(attrs={'class': 'checkbox'}),
                                      choices=DATE_HAPPENED_CHOICES,
                                      )
    match_rating = forms.ChoiceField(label=mark_safe("<p><strong>Please rate your match on a scale from 0 (bad) to 10 (perfect): </br> </strong> </p>"),
                                     choices=RATING_CHOICES)
    inappropriate_behavior = forms.ChoiceField(label=mark_safe("<strong>Report inappropriate behavior</strong>"),
                                               widget=forms.RadioSelect(
                                                   attrs={'label': 'Name', 'class': 'checkbox'}),
                                               choices=BEHAVIOR_CHOICES)

    match_comments = forms.CharField(label=mark_safe("<strong>Please use this section to provide any personal comments on how the date went. <br> (If you didn't attend, or the match behaved inappropriately, please provide additional details): </strong> "),
                                     widget=forms.Textarea(attrs={'class': 'textarea rows="8"'}))

    class Meta:
        model = Match_Feedback
        fields = ('date_happened',
                  'match_rating',
                  'inappropriate_behavior',
                  'match_comments',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = "" # Hide the body lable
        self.fields['body'].widget.attrs = {'placeholder': 'Enter text here...', 'class':'form-control', 'rows':'2'}
