from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def chatPage(request, chat_box_name, *args, **kwargs):
	context = {'chat_box_name': chat_box_name}
	return render(request, "chat/chatPage.html", context)
