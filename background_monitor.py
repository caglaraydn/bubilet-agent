import time
import json
from datetime import datetime
import config
from one_time_check import get_ticket_data, send_telegram

STOCK_FILE = 'stok_durumu.json'

def load_previous_stock():
    """Loads previous stock data from the JSON file."""
    try:
        with open(STOCK_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_current_stock(data):
    """Saves current stock data to the JSON file."""
    try:
        with open(STOCK_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving stock data: {e}")

def monitor_tickets():
    print(f"Starting background monitor for: {config.API_URL}")
    print(f"Check Interval: {config.CHECK_INTERVAL} seconds")
    print("Press Ctrl+C to stop.")
    
    # Startup Notification
    current_time = datetime.now().strftime("%H:%M:%S")
    current_stock = get_ticket_data()
    
    if current_stock is not None:
        startup_msg_lines = [f"🚀 Sistem Başlatıldı ve Takipte! ({current_time})", ""]
        for name, data in current_stock.items():
            count = data.get("count", 0)
            price = data.get("price", 0.0)
            startup_msg_lines.append(f"🎫 {name} ({price} TL): {count} adet")
        
        send_telegram("\n".join(startup_msg_lines))
        
        # Initialize previous stock from file
        previous_stock = load_previous_stock()
        
        # If file was empty but we have current stock, save it as initial state
        if not previous_stock:
             save_current_stock(current_stock)
             previous_stock = current_stock
    else:
        print("Failed to fetch initial ticket data.")
        previous_stock = {}

    while True:
        try:
            current_stock = get_ticket_data()
            current_time = datetime.now().strftime("%H:%M:%S")
            
            if current_stock is not None:
                print(f"\n--- [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Kontrol Yapıldı ---")
                for name, data in current_stock.items():
                    count = data.get("count", 0)
                    price = data.get("price", 0.0)
                    print(f" • {name}: {count} adet ({price} TL)")

                if previous_stock:
                    for name, current_data in current_stock.items():
                        # Handle old format (integer) vs new format (dict)
                        prev_data = previous_stock.get(name, {})
                        if isinstance(prev_data, int):
                            previous_count = prev_data
                        else:
                            previous_count = prev_data.get("count", 0)
                        
                        current_count = current_data.get("count", 0)
                        current_price = current_data.get("price", 0.0)
                        
                        # Check if tickets were sold (previous > current)
                        if previous_count > current_count:
                            diff = previous_count - current_count
                            message = (
                                f"🔔 Hareket Algılandı!\n\n"
                                f"🎫 {name} ({current_price} TL): {diff} adet bilet satıldı!\n"
                                f"Güncel Stok: {current_count}"
                            )
                            print(f"[{current_time}] {message}")
                            send_telegram(message)
                
                # Update previous stock and save to file
                previous_stock = current_stock
                save_current_stock(current_stock)
            else:
                print(f"\n--- [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Kontrol Yapıldı ---")
                print("⚠️ Veri çekilemedi!")
                
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Unexpected Error in loop: {e}")
            
        time.sleep(config.CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_tickets()
