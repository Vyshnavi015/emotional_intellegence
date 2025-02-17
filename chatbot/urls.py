
from django.urls import path
from . import views

urlpatterns = [
    path('chatbot/', views.chatbot_interface, name='chatbot_interface'),
    path('chat/', views.chatbot_response, name='chatbot_response'),
]

