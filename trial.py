from openai import OpenAI

import time
from gtts import gTTS
import os
from dotenv import load_dotenv
import pyttsx3
import base64


load_dotenv()


# Set up OpenAI API key
# openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_chatgpt_response(prompt):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content

def get_chatgpt_audio_response(prompt):
    completion = openai.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "onyx", "format": "wav"},
        messages=[
        {
            "role": "user",
            "content": prompt
        }
        ]
    )
    wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
    with open("response.wav", "wb") as f:
        f.write(wav_bytes)
        
    # play the audio
    os.system("afplay response.wav")



def text_to_speech(text):
    tts = gTTS(text=text, lang='en', tld='us')
    tts.save("response.mp3")
    # os.system("mpg321 response.mp3")
    # play on a macbook
    os.system("afplay response.mp3")
    
def text_to_speech_pyttsx3(text):
    # engine = pyttsx3.init()
    # engine.say(text)
    # engine.runAndWait()
    
    #Starting microsoft speech api sapi5
    engine = pyttsx3.init()
    # voices = engine.getProperty('voices') #fetching different voices from the system
    # engine.setProperty('voice', voices[1].id) #setting voice properties
    engine.setProperty('rate', 130) #sets speed of speech

    engine.say(text)
    engine.runAndWait()
    


        

def main():
    while True:
        # we will be getting data from pump fun here, this is just a placeholder
        # user_input = input("Enter your question: ")
        
        # Get response from ChatGPT
        # response = get_chatgpt_response(user_input)
   
        
        # # Convert response to speech and move mouth
        # words = response.split()
        # for word in words:
        #     move_mouth()
        #     time.sleep(0.2)
        
        # Speak the response
        # text_to_speech(response)
        # response = "Hello, how are you?"
        # text_to_speech_pyttsx3(response)
        response = get_chatgpt_audio_response("Hello, how are you?")


        
if __name__ == "__main__":
    try:
        main()
    finally:
        print("Cleaning up GPIO")
        # GPIO.cleanup()