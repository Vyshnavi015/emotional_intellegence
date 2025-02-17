# chatbot/model_integration.py
from transformers import pipeline

# Load sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

# Load text generation model (GPT-2)
text_generator = pipeline("text-generation", model="gpt2")

def analyze_sentiment(text):
    return sentiment_analyzer(text)

def generate_text(prompt):
    return text_generator(prompt, max_length=100)
