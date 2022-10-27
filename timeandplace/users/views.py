from django.shortcuts import render,redirect
from .forms import NewUserForm, ProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
# from django.http import HttpResponse


def index(request):
    return render(request=request, template_name = "users/home.html")

def home(request):
    return render(request=request, template_name="users/home.html")

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			form.save()
			# login(request, user)
			messages.success(request, "Registration successful." )
			username = form.cleaned_data.get("username")
			messages.success(request, f"Account Created. You can now log in {username}")
			return redirect("login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	else:
		form = NewUserForm()
	return render (request=request, template_name="users/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("main:index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="users/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("main:index")

# Add profile view
def profile(request):
	context = {'profile_form': ProfileForm()}
	return render(request, template_name='users/profile.html', context=context)