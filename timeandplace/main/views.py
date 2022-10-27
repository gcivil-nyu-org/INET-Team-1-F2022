from django.shortcuts import render
# from django.contrib.auth import login, authenticate, logout
# from django.contrib import messages
# from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
# from django.http import HttpResponse


def index(request):
    return render(request=request, template_name="main/home.html")

def home(request):
    return render(request=request, template_name="main/home.html")