from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_interface, name='chatbot_home'),  # This makes /bot/ work
    path('i/', views.chatbot_interface, name='chatbot_interface'),  # Loads chat.html
    path('chat/', views.chatbot_response, name='chatbot_response'),  # Handles chatbot messages
]



