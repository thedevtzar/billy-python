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



# Load environment variables
load_dotenv('gpio.env')

# # Set up GPIO pins for Billy Bass control
# MOTOR_MOUTH_ENA = int(os.getenv('MOTOR_MOUTH_ENA'))
# MOTOR_MOUTH_IN1 = int(os.getenv('MOTOR_MOUTH_IN1'))
# MOTOR_MOUTH_IN2 = int(os.getenv('MOTOR_MOUTH_IN2'))
# MOTOR_BODY_IN3 = int(os.getenv('MOTOR_BODY_IN3'))
# MOTOR_BODY_IN4 = int(os.getenv('MOTOR_BODY_IN4'))
# MOTOR_BODY_ENB = int(os.getenv('MOTOR_BODY_ENB'))
# AUDIO_DETECTOR = int(os.getenv('AUDIO_DETECTOR'))

MOTOR_MOUTH_ENA=7     # Physical pin 7 (GPIO 4)
MOTOR_MOUTH_IN1=11    # Physical pin 11 (GPIO 17)
MOTOR_MOUTH_IN2=13    # Physical pin 13 (GPIO 27)
MOTOR_BODY_IN3=15     # Physical pin 15 (GPIO 22)
MOTOR_BODY_IN4=16     # Physical pin 16 (GPIO 23)
MOTOR_BODY_ENB=18     # Physical pin 18 (GPIO 24)
AUDIO_DETECTOR=29     # Physical pin 29 (GPIO 5)



print(MOTOR_MOUTH_ENA, MOTOR_MOUTH_IN1, MOTOR_MOUTH_IN2, MOTOR_BODY_IN3, MOTOR_BODY_IN4, MOTOR_BODY_ENB, AUDIO_DETECTOR)

GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
GPIO.setup(MOTOR_MOUTH_ENA, GPIO.OUT)
GPIO.setup(MOTOR_MOUTH_IN1, GPIO.OUT)
GPIO.setup(MOTOR_MOUTH_IN2, GPIO.OUT)
GPIO.setup(MOTOR_BODY_IN3, GPIO.OUT)
GPIO.setup(MOTOR_BODY_IN4, GPIO.OUT)
GPIO.setup(MOTOR_BODY_ENB, GPIO.OUT)
GPIO.setup(AUDIO_DETECTOR, GPIO.IN)


# GPIO.setmode(GPIO.BCM)
# GPIO.setup(MOUTH_PIN, GPIO.OUT)
# GPIO.setup(HEAD_PIN, GPIO.OUT)
# GPIO.setup(TAIL_PIN, GPIO.OUT)

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

def move_mouth():
    # GPIO.output(MOUTH_PIN, GPIO.HIGH)
    GPIO.output(MOTOR_MOUTH_ENA, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(MOTOR_MOUTH_ENA, GPIO.LOW)

def move_head():
    # GPIO.output(HEAD_PIN, GPIO.HIGH)
    GPIO.output(MOTOR_BODY_IN3, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(MOTOR_BODY_IN3, GPIO.LOW)

def move_tail():
    # GPIO.output(TAIL_PIN, GPIO.HIGH)
    GPIO.output(MOTOR_BODY_IN4, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(MOTOR_BODY_IN4, GPIO.LOW)

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