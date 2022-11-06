# Create your models here.
from django.db import models
from django.conf import settings
import datetime
from datetime import date

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    date_of_birth = models.DateField(blank=True, null=True, default=date.today())
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                        blank=True,
                        default='users/default/user-default.png')
    occupation = models.CharField(max_length = 50,blank=True, null=True)
    proposal_time = models.CharField(max_length = 50,blank=True, null=True)
    proposal_location = models.CharField(max_length = 50,blank=True, null=True)
    about_me = models.CharField(max_length = 100,blank=True, null=True)
    gender_choices = (('Woman', 'Woman'), ('Man', 'Man'), ('Transgender', 'Transgender'), ('Non-binary', 'Non-binaary'))
    gender_identity = models.CharField(max_length = 15, choices = gender_choices, blank = True, default="N/A")
    orientation_choices = (('Lesbian', 'Lesbian'), ('Gay', 'Gay'), ('Bisexual', 'Bisexual'), ('Queer', 'Queer'), ('Asexual', 'Asexual'), ('Straight', 'Straight'),('Other', 'Other'))
    sexual_orientation = models.CharField(max_length = 15, choices = orientation_choices, blank = True, default="N/A")
    age_preference_min = models.IntegerField(blank=True, null=True)
    age_preference_max = models.IntegerField(blank=True, null=True)
    gender_preference = models.CharField(max_length = 15, choices = gender_choices, blank = True)
    orientation_preference = models.CharField(max_length = 15, choices = orientation_choices, blank = True)
    # age = models.IntegerField(blank=True, null=True)
    # age = datetime.datetime.now() - date_of_birth
    # marital_choices = (('Single', 'Single'), ('Widowed', 'Widowed'), ('Married', 'Married'), ('Unmarried', 'Unmarried'), ('Divorced', 'Divorced'))
    # marital_status = models.CharField(max_length = 10, choices = marital_choices, blank = True)

    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='users_liked', blank=True)
    @property
    def calc_age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    def __str__(self):
        return f'Profile for user {self.user.username}'

