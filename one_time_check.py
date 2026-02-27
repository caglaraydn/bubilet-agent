import requests
from datetime import datetime
import config

def get_ticket_data():
    """Fetches ticket data from the API."""
    try:
        response = requests.get(config.API_URL, headers=config.HEADERS)
        response.raise_for_status()
        
        data = response.json()
        session_tickets = data.get("sessionTickets", [])
        
        ticket_data = {}
        for ticket in session_tickets:
            seat_group_name = ticket.get("seatGroupName", "Unknown Category")
            remaining_tickets = ticket.get("remainingTickets", 0)
            price = ticket.get("price", 0.0)
            ticket_data[seat_group_name] = {
                "count": remaining_tickets,
                "price": price
            }
            
        return ticket_data
        
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Network Error: {e}")
        return None
    except ValueError as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] JSON Parsing Error: {e}")
        return None
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Unexpected Error: {e}")
        return None

def send_telegram(text):
    """Sends a message to the configured Telegram chat."""
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": text
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Telegram mesajı gönderildi.")
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Telegram Error: {e}")
        if response is not None:
             print(f"Telegram Response: {response.text}")

if __name__ == "__main__":
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"[{current_time}] Checking tickets...")
    
    tickets = get_ticket_data()
    
    if tickets:
        message_lines = [f"🔔 Stok Raporu ({current_time})", ""]
        for name, data in tickets.items():
            count = data.get("count", 0)
            price = data.get("price", 0.0)
            line = f"🎫 {name} ({price} TL): {count} adet"
            print(line)
            message_lines.append(line)
            
        send_telegram("\n".join(message_lines))
    else:
        print("Failed to fetch ticket data.")
