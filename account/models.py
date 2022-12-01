# Create your models here.
from django.db import models
from django.conf import settings
import datetime
from datetime import date
#from smart_selects.db_fields import ChainedForeignKey


class Location(models.Model):
    DBA = models.CharField(max_length=255,blank=True,null=True)
    BORO = models.CharField(max_length=255,blank=True,null=True) 
    BUILDING = models.CharField(max_length=255,blank=True,null=True)
    STREET = models.CharField(max_length = 255,blank=True,null=True)
    ZIPCODE = models.CharField(max_length=255,blank=True,null=True)
    PHONE = models.CharField(max_length=255,blank=True,null=True)
    CUISINE = models.CharField(max_length=255,blank=True,null=True)
    LATITUDE = models.CharField(max_length=255,blank=True,null=True)
    LONGITUDE = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return f'{self.DBA} At : {self.BUILDING}, {self.STREET}, {self.BORO} '

class Boro(models.Model):
    boro = models.CharField(max_length=255,blank=True,null=True)
    def __str__(self):
        return self.boro

class Cusine(models.Model):
    cusine = models.CharField(max_length=255,blank=True,null=True)
    def __str__(self):
        return self.cusine


class newLocation(models.Model):
    DBA = models.CharField(max_length=255,blank=True,null=True)
    BORO = models.ForeignKey(Boro,on_delete=models.SET_NULL, blank=True, null=True) 
    BUILDING = models.CharField(max_length=255,blank=True,null=True)
    STREET = models.CharField(max_length = 255,blank=True,null=True)
    ZIPCODE = models.CharField(max_length=255,blank=True,null=True)
    PHONE = models.CharField(max_length=255,blank=True,null=True)
    CUISINE = models.ForeignKey(Cusine,on_delete=models.SET_NULL, blank=True, null=True)
    LATITUDE = models.CharField(max_length=255,blank=True,null=True)
    LONGITUDE = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return f'{self.DBA} At : {self.BUILDING}, {self.STREET}, {self.BORO} '



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    date_of_birth = models.DateField(blank=True, null=True, default=date.today())
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                        blank=True,
                        default='users/default/user-default.png')
    occupation = models.CharField(max_length = 50,blank=True, null=True)
    #proposal_time = models.CharField(max_length = 50,blank=True, null=True)
    #proposal_datetime = models.DateTimeField(blank=True, null=True)
    # proposal_date_new = models.DateField(blank=True, null=True)
    # proposal_time_new = models.TimeField(blank=True, null=True)
    proposal_datetime_local = models.DateTimeField(blank=True, null=True)
    # proposal_location = models.CharField(max_length = 50,blank=True, null=True)
    about_me = models.CharField(max_length = 100,blank=True, null=True)
    gender_choices = (('Woman', 'Woman'), ('Man', 'Man'), ('Transgender', 'Transgender'), ('Non-binary', 'Non-binary'))
    gender_identity = models.CharField(max_length = 15, choices = gender_choices, blank = True, default="N/A")
<<<<<<< HEAD
    orientation_choices = (('Lesbian', 'Lesbian'), ('Gay', 'Gay'), ('Bisexual', 'Bisexual'), ('Queer', 'Queer'), ('Asexual', 'Asexual'), ('Straight', 'Straight'),('Other', 'Other'))
    sexual_orientation = models.CharField(max_length = 15, choices = orientation_choices, blank = True, default="N/A")
    age_preference_min = models.IntegerField(blank=True, null=True)
    age_preference_max = models.IntegerField(blank=True, null=True)
    gender_preference = models.CharField(max_length = 15, choices = gender_choices, blank = True)
    orientation_preference = models.CharField(max_length = 15, choices = orientation_choices, blank = True)
=======
    # orientation_choices = (('Lesbian', 'Lesbian'), ('Gay', 'Gay'), ('Bisexual', 'Bisexual'), ('Queer', 'Queer'), ('Asexual', 'Asexual'), ('Straight', 'Straight'),('Other', 'Other'))
    # sexual_orientation = models.CharField(max_length = 15, choices = orientation_choices, blank = True, default="N/A")
    age_preference_min = models.PositiveIntegerField(blank=True, null=True, default= 19, validators=[MinValueValidator(18), MaxValueValidator(100)])
    age_preference_max = models.PositiveIntegerField(blank=True, null=True, default= 20,validators=[MinValueValidator(19), MaxValueValidator(100)])
    def clean(self):
        if self.age_preference_max < self.age_preference_min:
            raise ValidationError("Minimum age has be smaller or equal to the Maximum Age")
    gender_choices_pref = (('Woman', 'Woman'),('Man', 'Man'), ('Both', 'Both'), ('Transgender', 'Transgender'), ('Non-binary', 'Non-binary'))
    gender_preference = models.CharField(max_length = 15, choices = gender_choices_pref, blank = True)
    # orientation_preference = models.CharField(max_length = 15, choices = orientation_choices, blank = True)
>>>>>>> f430d74 (fixed sexual orientation bug)
    #location_drawdown = models.ForeignKey(Location,on_delete=models.SET_NULL, blank=True, null=True)
    boro = models.ForeignKey(Boro,on_delete=models.SET_NULL, blank=True, null=True)
    cusine = models.ForeignKey(Cusine,on_delete=models.SET_NULL, blank=True, null=True)
    location_dropdown  = models.ForeignKey(newLocation, on_delete=models.SET_NULL, blank=False, null=True)
    # age = models.IntegerField(blank=True, null=True)
    # age = datetime.datetime.now() - date_of_birth
    # marital_choices = (('Single', 'Single'), ('Widowed', 'Widowed'), ('Married', 'Married'), ('Unmarried', 'Unmarried'), ('Divorced', 'Divorced'))
    # marital_status = models.CharField(max_length = 10, choices = marital_choices, blank = True)
    # users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='users_liked', blank=True)
    likes = models.ManyToManyField(
        "self",
        related_name="liked_by",
        symmetrical=False,
        blank=True
    )
    hides = models.ManyToManyField(
        "self",
        related_name="hidden_by",
        symmetrical=False,
        blank=True
    )

    declines = models.ManyToManyField(
        "self",
        related_name="declined_by",
        symmetrical=False,
        blank=True
    )
    matches = models.ManyToManyField(
        "self",
        related_name="matched_with",
        symmetrical=False,
        blank=True
    )

    @property
    def calc_age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    def __str__(self):
        return f'Profile for user {self.user.username}'

