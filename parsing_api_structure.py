# Imports
import flet as ft 
import requests 
import os 
from murf import Murf 
from api_key import API_KEY
import pathlib 

# API Client
client = Murf(api_key=API_KEY)
voices = client.text_to_speech.get_voices()
for voice in voices:
    print(f"Voice ID: {voice.voice_id}, Name: {voice.display_name}, Moods: {voice.available_styles}")