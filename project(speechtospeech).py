import azure.cognitiveservices.speech as speechsdk
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

# Basic Setup
load_dotenv()

# Retrieve API keys and endpoint from environment variables
speech_key = os.getenv("SPEECH_API_KEY")
speech_region = os.getenv("SPEECH_REGION")
text_analytics_key = os.getenv("TEXT_ANALYTICS_KEY")
text_analytics_endpoint = os.getenv("TEXT_ANALYTICS_ENDPOINT")

def speech_to_text():
    # Configuring the speech recognizer
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak Now...")
    result = speech_recognizer.recognize_once()  
    # Recognize speech from the microphone
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: {result.text}")
        return result.text
    else:
        print("Speech not recognized. Please try again.")

def authenticate_client():
    # Create a Text Analytics client
    credential = AzureKeyCredential(text_analytics_key)
    text_analytics_client = TextAnalyticsClient(endpoint=text_analytics_endpoint, credential=credential)
    return text_analytics_client

def analyze_sentiment(text):
    # Analyze sentiment of the provided text
    client = authenticate_client()
    documents = [text]  # Prepare the document for analysis
    response = client.analyze_sentiment(documents=documents)[0]
    print(f"Detected Sentiment: {response.sentiment}")
    return response.sentiment

# Corrected the conditional to use double underscores
if __name__ == "__main__":
    recognized_text = speech_to_text()  # Convert speech to text
    if recognized_text:
        sentiment = analyze_sentiment(recognized_text)  # Analyze the sentiment of the recognized text
        if sentiment:
            print(f"Sentiment: {sentiment}")  # Print the sentiment result
