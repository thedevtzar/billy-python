from openai import OpenAI
import RPi.GPIO as GPIO
import time
from gtts import gTTS
import os
from dotenv import load_dotenv

load_dotenv()

# Set up OpenAI API key
openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
# Set up GPIO pins for Billy Bass control

MOUTH_PIN = 17
HEAD_PIN = 18
TAIL_PIN = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOUTH_PIN, GPIO.OUT)
GPIO.setup(HEAD_PIN, GPIO.OUT)
GPIO.setup(TAIL_PIN, GPIO.OUT)

def get_chatgpt_response(prompt):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response.choices[0].message

def move_mouth():
    GPIO.output(MOUTH_PIN, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(MOUTH_PIN, GPIO.LOW)

def move_head():
    GPIO.output(HEAD_PIN, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(HEAD_PIN, GPIO.LOW)

def move_tail():
    GPIO.output(TAIL_PIN, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(TAIL_PIN, GPIO.LOW)

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")

def main():
    while True:
        # we will be getting data from pump fun here, this is just a placeholder
        user_input = input("Enter your question: ")
        
        # Get response from ChatGPT
        response = get_chatgpt_response(user_input)
        
        print(response)
        
        # Move Billy Bass
        move_head()
        move_tail()
        
        # Convert response to speech and move mouth
        words = response.split()
        for word in words:
            move_mouth()
            time.sleep(0.2)
        
        # Speak the response
        text_to_speech(response)

if __name__ == "__main__":
    try:
        main()
    finally:
        # print("Cleaning up GPIO")
        GPIO.cleanup()