from django.http import JsonResponse
from django.shortcuts import render
from .models import Conversation
from transformers import pipeline

# Initialize models
sentiment_analyzer = pipeline("sentiment-analysis")
text_generator = pipeline("text-generation", model="gpt2")  # Change model if needed

def generate_response(user_message):
    """Generates chatbot response based on sentiment analysis and text generation"""
    bot_response = "I didn’t quite understand that. Can you clarify?"  # Default fallback response

    try:
        # Perform sentiment analysis
        sentiment_result = sentiment_analyzer(user_message)[0]
        sentiment = sentiment_result['label']

        # Generate response based on sentiment
        if sentiment == "POSITIVE":
            bot_response = "I'm so glad you're feeling good! Keep it up!"
        elif sentiment == "NEGATIVE":
            bot_response = "I'm really sorry you're feeling this way. It's okay to feel down sometimes."
        else:
            bot_response = "I can see you're going through something. I'm here to help."

        # If user is sad or wants to talk, generate a response
        if 'sad' in user_message or 'talk' in user_message:
            prompt = f"Generate a short, supportive response to someone who's feeling sad: {user_message}"
            generated_response = text_generator(prompt, max_length=50, num_return_sequences=1)
            if generated_response:
                bot_response += "\n\n" + generated_response[0].get('generated_text', "I'm here for you.")
    
    except Exception as e:
        print(f"Error in generate_response: {e}")

    return bot_response

def detect_emotion(user_message):
    """Detects emotion based on keywords"""
    if "sad" in user_message or "alone" in user_message:
        return "sadness"
    elif "happy" in user_message or "excited" in user_message:
        return "joy"
    elif "angry" in user_message or "frustrated" in user_message:
        return "anger"
    elif "scared" in user_message or "fear" in user_message:
        return "fear"
    else:
        return "neutral"

def chatbot_response(request):
    """Handles user messages and generates chatbot responses"""
    if request.method == "GET":
        user_message = request.GET.get('message', "").strip()

        if user_message:
            bot_response = generate_response(user_message)
            emotion = detect_emotion(user_message)

            # Save conversation to database
            Conversation.objects.create(
                user_message=user_message,
                bot_response=bot_response,
                feedback=1,  # Default feedback value
                emotion=emotion
            )

            # Return response as JSON
            return JsonResponse({'response': bot_response, 'emotion': emotion})

    return JsonResponse({'response': "Sorry, I couldn't understand that.", 'emotion': "neutral"})

def chatbot_interface(request):
    """Render the chatbot interface"""
    return render(request, 'chat.html')
