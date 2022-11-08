from django.contrib import admin

from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user_id', 'id','user', 'date_of_birth', 'photo', 'liked_by']