from transformers import pipeline

# Load the pre-trained emotion classification model
emotion_classifier = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions")

'''def detect_emotion(user_input):
    result = emotion_classifier(user_input)
    emotion = result[0]['label']  # Ensure that we extract just the label (string) from the dict
    return emotion  # This should return a string, not a dict'''

# A simple example of emotion detection logic
def detect_emotion(user_message):
    # For now, this is a basic example of emotion detection based on keywords
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
