# Create your models here.
from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                        blank=True)
    occupation = models.CharField(max_length = 50,blank=True, null=True)
    proposal_time = models.CharField(max_length = 50,blank=True, null=True)
    proposal_location = models.CharField(max_length = 50,blank=True, null=True)
    about_me = models.CharField(max_length = 100,blank=True, null=True)
    def __str__(self):
        return f'Profile for user {self.user.username}'