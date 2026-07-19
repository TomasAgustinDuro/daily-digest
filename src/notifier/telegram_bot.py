from dotenv import load_dotenv
import os
import httpx

load_dotenv()

def send_message(summary: str):
    url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
    payload = {
        "chat_id": os.getenv('TELEGRAM_CHAT_ID'),
        "text": summary
    }

    response = httpx.post(url, json=payload)

    if response.is_success:
        print("Mensaje enviado a Telegram correctamente")
    else:
        print(f"Error enviando a Telegram: {response.status_code} - {response.text}")


if __name__ == "__main__":
    send_message("Mensaje de prueba desde NBA Daily Digest 🏀")