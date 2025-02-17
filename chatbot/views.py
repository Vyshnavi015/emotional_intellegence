from django.http import JsonResponse
from .emotion_detection import detect_emotion
import random
'''
# A simple memory of user context (this can be expanded to a more robust system if needed)
user_context = {}

def chatbot_response(request):
    if request.method == "GET":
        user_message = request.GET.get("message", "")
        user_id = request.GET.get("user_id", "user1")  # Assuming user_id is passed in the query params

        # Detect the emotion in the user's message
        emotion = detect_emotion(user_message)

        # Store the user's emotional state in memory for this session
        user_context[user_id] = user_context.get(user_id, {})
        user_context[user_id]['last_emotion'] = emotion

        # Responses based on detected emotion
        responses = {
            "sadness": [
                "I’m really sorry you're feeling this way. You're not alone. 💙",
                "It’s okay to feel sad sometimes. Would you like to talk more about it?",
                "I understand, and I’m here for you. Sometimes, a little mindfulness or breathing helps."
            ],
            "joy": [
                "That's amazing! Keep that energy up! 😊 What made you feel this way?",
                "I'm so glad to hear that! Is there something special you want to share?",
                "Great to hear you're feeling happy! Remember to cherish these moments!"
            ],
            "anger": [
                "I can feel your frustration. It's okay to be angry, but don't let it take over.",
                "Anger can be tough to handle. Maybe a quick break or some breathing exercises can help. Want to try it?",
                "I can sense your frustration. Let’s breathe together. Inhale... Exhale... Feel better?"
            ],
            "fear": [
                "Fear can be really overwhelming. It's okay to feel scared, but you’re stronger than you think.",
                "I understand you're feeling afraid. But remember, it's okay to take small steps to overcome it.",
                "It's normal to have fear, but don't let it control you. Sometimes a calming exercise can help you."
            ],
            "neutral": [
                "I’m here to listen if you want to share more. How can I help you today?",
                "I see you're feeling okay right now. Would you like to chat or ask for advice on something?",
                "It's great to hear you’re feeling neutral! Sometimes balance is the best state."
            ]
        }

        # Personalized dynamic responses based on user context
        if emotion == "sadness":
            if user_context[user_id].get('last_emotion') == "joy":
                # Provide advice: Transition from joy to sadness
                advice = "Remember, emotions are like waves. It's okay to feel ups and downs. Take things one step at a time."
            else:
                advice = "When you're feeling down, doing things you love or practicing mindfulness can really help."

        elif emotion == "anger":
            advice = "Would you like to try a quick breathing exercise to release that tension?"

        elif emotion == "fear":
            advice = "Sometimes, facing small fears gradually can help you overcome them. What small step can you take today?"

        else:
            advice = "Stay positive and keep looking for things that bring you peace."

        # Select a response based on emotion and combine with advice
        bot_response = random.choice(responses.get(emotion, responses["neutral"]))
        bot_message = f"{bot_response} \nHere's some advice: {advice}"

        return JsonResponse({"response": bot_message, "emotion": emotion})'''
'''
from django.http import JsonResponse
from .emotion_detection import detect_emotion  # Import the detect_emotion function
import random

user_context = {}

def chatbot_response(request):
    if request.method == "GET":
        user_message = request.GET.get("message", "")
        user_id = request.GET.get("user_id", "user1")

        # Use the detect_emotion function to determine the user's emotion
        emotion = detect_emotion(user_message)

        # Store the user's emotional state in memory
        user_context[user_id] = user_context.get(user_id, {})
        user_context[user_id]['last_emotion'] = emotion

        responses = {
            "sadness": [
                "I’m really sorry you're feeling this way. You're not alone. 💙",
                "It’s okay to feel sad sometimes. Would you like to talk more about it?",
                "I understand, and I’m here for you. Sometimes, a little mindfulness or breathing helps."
            ],
            "joy": [
                "That's amazing! Keep that energy up! 😊 What made you feel this way?",
                "I'm so glad to hear that! Is there something special you want to share?",
                "Great to hear you're feeling happy! Remember to cherish these moments!"
            ],
            "anger": [
                "I can feel your frustration. It's okay to be angry, but don't let it take over.",
                "Anger can be tough to handle. Maybe a quick break or some breathing exercises can help. Want to try it?",
                "I can sense your frustration. Let’s breathe together. Inhale... Exhale... Feel better?"
            ],
            "fear": [
                "Fear can be really overwhelming. It's okay to feel scared, but you’re stronger than you think.",
                "I understand you're feeling afraid. But remember, it's okay to take small steps to overcome it.",
                "It's normal to have fear, but don't let it control you. Sometimes a calming exercise can help you."
            ],
            "neutral": [
                "I’m here to listen if you want to share more. How can I help you today?",
                "I see you're feeling okay right now. Would you like to chat or ask for advice on something?",
                "It's great to hear you’re feeling neutral! Sometimes balance is the best state."
            ]
        }

        # Personalized dynamic responses based on user context
        if emotion == "sadness":
            if user_context[user_id].get('last_emotion') == "joy":
                advice = "Remember, emotions are like waves. It's okay to feel ups and downs. Take things one step at a time."
            else:
                advice = "When you're feeling down, doing things you love or practicing mindfulness can really help."

        elif emotion == "anger":
            advice = "Would you like to try a quick breathing exercise to release that tension?"

        elif emotion == "fear":
            advice = "Sometimes, facing small fears gradually can help you overcome them. What small step can you take today?"

        else:
            advice = "Stay positive and keep looking for things that bring you peace."

        # Select a response based on emotion and combine with advice
        bot_response = random.choice(responses.get(emotion, responses["neutral"]))
        bot_message = f"{bot_response} \n {advice}"

        return JsonResponse({"response": bot_message, "emotion": emotion})'''

from django.shortcuts import render
from django.http import JsonResponse
from .emotion_detection import detect_emotion
from transformers import pipeline

# Initialize the sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")
# Initialize the text generation model (GPT-2 or similar)
text_generator = pipeline("text-generation", model="gpt2")



def chatbot_interface(request):
    return render(request,'chat.html')

def chatbot_response(request):
    user_message = request.GET.get('message')

    if user_message:
        # Perform sentiment analysis on the user's message
        sentiment_result = sentiment_analyzer(user_message)[0]
        sentiment = sentiment_result['label']

        # Generate a response based on sentiment
        if sentiment == "POSITIVE":
            bot_response = "I'm so glad you're feeling good! Keep it up!"
        elif sentiment == "NEGATIVE":
            bot_response = "I'm really sorry you're feeling this way. It's okay to feel down sometimes."
        else:
            bot_response = "I can see you're going through something. I'm here to help."
        
        if 'sad' in user_message or 'talk' in user_message:
            prompt = f"Generate a short, supportive response to someone who's feeling sad: {user_message}"
            generated_response = text_generator(prompt, max_length=50, num_return_sequences=1)
        else:
            bot_response = "I didn’t quite understand that. Can you clarify?"


        # Use GPT-2 for a dynamic, but concise generative response
        #generated_response = text_generator(user_message, max_length=50, num_return_sequences=1)
        bot_response += "\n\n" + generated_response[0]['generated_text']

        return JsonResponse({"bot_response": bot_response})
    else:
        return JsonResponse({"bot_response": "I didn't quite get that. Can you try again?"})

