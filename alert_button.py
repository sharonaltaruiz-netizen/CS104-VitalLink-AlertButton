
import time
import os
import requests
import RPi.GPIO as GPIO
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_alert():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": "Someone pressed the alert button!"
    }

    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        print("Telegram alert sent successfully!")
    except requests.RequestException as error:
        print("Error sending Telegram alert:", error)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Alert button monitoring system is now active. Press Ctrl+C to stop.")

button_pressed = False

try:
    while True:
        if GPIO.input(7) == GPIO.HIGH and not button_pressed:
            print("Someone pressed the alert button!")
            send_telegram_alert()
            button_pressed = True
        elif GPIO.input(7) == GPIO.LOW:
            button_pressed = False
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")
finally:
    GPIO.cleanup()
