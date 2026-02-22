import sqlite3
import json
import os
from datetime import datetime

# --- KONFIGURACJA ---
DB_NAME = "wow_market.db"
JSON_DIR = "Archive"
WATCHLIST = [190321, 190324, 210933]

def init_db():
    """Tworzy bazę i tabele, jeśli nie istnieją"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS price_history
                 (timestamp TEXT, item_id INTEGER, min_price INTEGER, quantity INTEGER)''')
    conn.commit()
    conn.close()

def process_json(file_path):
    """Wyciąga esencję z ogromnego JSONa i wkłada do bazy"""
    filename = os.path.basename(file_path)
    time_str = filename.replace('.json', '').replace('_', ' ')
    
    with open(file_path, 'r') as f:
        try:
            auctions = json.load(f)
        except json.JSONDecodeError:
            print(f"❌ Plik {filename} jest uszkodzony.")
            return

    extracted_data = []
    
    for item_id in WATCHLIST:
        item_auctions = [a for a in auctions if a['item']['id'] == item_id]
        
        if item_auctions:
            min_p = min(a['unit_price'] for a in item_auctions)
            total_q = sum(a['quantity'] for a in item_auctions)

            extracted_data.append((time_str, item_id, min_p, total_q))

    return extracted_data

def main():
    init_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    files = [f for f in os.listdir(JSON_DIR) if f.endswith('.json')]
    print(f"🔍 Znaleziono {len(files)} plików do przetworzenia.")

    for f_name in files:
        full_path = os.path.join(JSON_DIR, f_name)
        data = process_json(full_path)
        
        if data:
            c.executemany("INSERT INTO price_history VALUES (?,?,?,?)", data)
            print(f"✅ Przetworzono: {f_name}")
            
    
    conn.commit()
    conn.close()
    print("\n🚀 Baza danych zaktualizowana!")

if __name__ == "__main__":
    main()