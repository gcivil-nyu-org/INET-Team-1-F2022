from django.contrib import admin

from .models import Profile,Cusine,newLocation,Boro,Match_Feedback


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user_id', 'id','user', 'date_of_birth', 'photo']



@admin.register(newLocation)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['DBA','BORO', 'BUILDING','STREET','ZIPCODE','PHONE','CUISINE','LATITUDE','LONGITUDE']

@admin.register(Cusine)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['cusine']

@admin.register(Boro)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['boro']


@admin.register(Match_Feedback)
class MatchFeedbackAdmin(admin.ModelAdmin):
    list_display = ['feedback_user', 'matched_user', 'match_date','match_location','date_happened',
                'match_rating',
                'inappropriate_behavior',
                ]     

