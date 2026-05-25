import os
import requests
from bs4 import BeautifulSoup

def send_telegram_message(message):
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("Telegram credentials not found in environment variables. Message not sent.")
        return
        
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram message sent successfully!")
        else:
            print(f"Failed to send message: {response.text}")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def check_fgv():
    url = "https://conhecimento.fgv.br/concursos/cfc"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        text = response.text.lower()
        
        if "2º exame" in text and "2026" in text or "2/2026" in text:
            return True, url
    except Exception as e:
        print(f"Error checking FGV: {e}")
    return False, ""

def check_cfc():
    url = "https://cfc.org.br/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        text = response.text.lower()
        
        if "2º exame de suficiência de 2026" in text or "exame de suficiência 2/2026" in text:
            return True, url
    except Exception as e:
        print(f"Error checking CFC: {e}")
    return False, ""

def main():
    print("Checking for 2º Exame de Suficiência de 2026...")
    found_fgv, url_fgv = check_fgv()
    found_cfc, url_cfc = check_cfc()
    
    if true    
        sources = [s for s in [url_fgv, url_cfc] if s]
        message = (
            "🚨 *ALERTA CFC* 🚨\n\n"
            "O edital do *2º Exame de Suficiência de 2026* aparentemente foi publicado ou atualizado nas páginas oficiais!\n\n"
            f"Verifique os links abaixo para consultar a data da prova e período de inscrições:\n\n"
            f"{chr(10).join(sources)}"
        )
        send_telegram_message(message)
    else:
        print("Edital not found yet.")

if __name__ == "__main__":
    main()
