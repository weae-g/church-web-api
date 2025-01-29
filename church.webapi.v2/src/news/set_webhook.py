import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def set_webhook(url):
    webhook_url = f"{BASE_URL}/setWebhook"
    data = {"url": url}
    response = requests.post(webhook_url, json=data)
    print(response.json())

if __name__ == '__main__':
    set_webhook('http://127.0.0.1:5000/api/webhook/telegram')  # Replace with your actual HTTPS URL
