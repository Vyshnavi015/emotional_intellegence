from django.db import models

# Create your models here.

class Conversation(models.Model):
    user_message = models.TextField()  # Store the user's message
    bot_response = models.TextField()  # Store the bot's response
    feedback = models.IntegerField()  # 0 for negative feedback, 1 for positive feedback
    emotion = models.CharField(max_length=50, null=True, blank=True)  # Store detected emotion

    def __str__(self):
        return f"Conversation {self.id}"

