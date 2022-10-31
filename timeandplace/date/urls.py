from django.urls import path

from . import views
app_name = "date"

urlpatterns = [
    path('', views.datePage, name='datepage'),
]