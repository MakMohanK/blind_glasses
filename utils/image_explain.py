# ===============================================
# AI BLIND GLASSES - Real Time Scene Description
# Uses OpenAI API Key + Camera
# Author: ChatGPT for Mohan
# ===============================================

# Install Required Packages First:
# pip3 install opencv-python openai pyttsx3 pillow requests

import cv2
import base64
import time
import threading
import pyttsx3
from openai import OpenAI

# ==============================
# ENTER YOUR OPENAI API KEY HERE
# ==============================
client = OpenAI(api_key="YOUR OPENAI KEY")

# ==============================
# TEXT TO SPEECH ENGINE
# ==============================
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ==============================
# ENCODE IMAGE TO BASE64
# ==============================
def encode_image(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode("utf-8")

# ==============================
# ANALYZE IMAGE USING GPT-4o
# ==============================
def analyze_scene(frame):
    try:
        base64_image = encode_image(frame)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe this image for a blind person in simple short words. Mention obstacles, people, objects, doors, stairs, vehicles." # arush enhance this prompt for detection
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=100
        )

        text = response.choices[0].message.content
        print("AI:", text)
        speak(text)

    except Exception as e:
        print("Error:", e)

# ==============================
# MAIN CAMERA LOOP
# ==============================
def start_glasses():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera not found")
        return

    print("Blind Glasses Started...")
    print("Press Q to Quit")

    last_time = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow("Blind Glasses Camera", frame)

        # Every 5 seconds analyze image
        if time.time() - last_time > 5:
            threading.Thread(target=analyze_scene, args=(frame.copy(),)).start()
            last_time = time.time()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    speak("Blind glasses started")
    start_glasses()