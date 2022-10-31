from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from users.models import Profile
from .filters import UserFilter
from .models import Message
# from django.contrib.auth import login, authenticate, logout
# from django.contrib import messages
# from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
# from django.http import HttpResponse


def index(request):
    return render(request=request, template_name="main/home.html")

def home(request):
    return render(request=request, template_name="main/home.html")

@login_required
def datePage(request):
    users = Profile.objects.all()
    user = request.user
    unreadMessages = Message.objects.filter(
        receiver=user).filter(status=False).count()

    myFilter = UserFilter(request.GET, queryset=users)
    users = myFilter.qs

    context = {
        'users': users,
        'userIn': user,
        'filter': myFilter,
        'unreadmsgs': unreadMessages
    }
    return render(request, "main/match-page.html", context)

class UserDetail(LoginRequiredMixin, DetailView):
    model = Profile
