
from django.shortcuts import render, redirect

def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("account/login/")
    context = {}
    return render(request, "chat/chatPage.html", context)
