from django.urls import path, include
from chat import views as chat_views

urlpatterns = [
    path("<str:chat_box_name>", chat_views.chatPage, name="chat-page"),
]