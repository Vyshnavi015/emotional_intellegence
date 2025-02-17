from transformers import pipeline

# Load the pre-trained emotion classification model
emotion_classifier = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions")

def detect_emotion(user_input):
    result = emotion_classifier(user_input)
    emotion = result[0]['label']  # Ensure that we extract just the label (string) from the dict
    return emotion  # This should return a string, not a dict
