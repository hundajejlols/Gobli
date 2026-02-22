import sqlite3
import json
import os
import shutil
from datetime import datetime

# --- CONFIGURATION ---
DB_NAME = "wow_market.db"
JSON_DIR = "archive"             
OLD_DIR = os.path.join(JSON_DIR, "old")  

# List of item IDs you are interested in
WATCHLIST = [190321, 190324, 210933, 190316] 

def init_db():
    """Creates database and table if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            timestamp TEXT,
            item_id INTEGER,
            min_price INTEGER,
            quantity INTEGER
        )''')
    conn.commit()
    conn.close()

def process_json(file_path):
    """Extracts key data from a JSON file handling both dict and list formats."""
    filename = os.path.basename(file_path)
    
    try:
        time_str = filename.replace('.json', '').replace('_', ' ')
    except:
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            # Fix: Check if data is a list or a dictionary
            if isinstance(data, dict):
                auctions = data.get('auctions', [])
            elif isinstance(data, list):
                auctions = data
            else:
                auctions = []
        except json.JSONDecodeError:
            print(f"Error: File {filename} is corrupted and will be skipped.")
            return None

    extracted_records = []

    for item_id in WATCHLIST:
        # Filter auctions for specific item ID
        item_auctions = [a for a in auctions if a.get('item', {}).get('id') == item_id]
        
        if item_auctions:
            # Get the lowest unit_price
            prices = [a.get('unit_price', a.get('buyout', 0)) for a in item_auctions]
            valid_prices = [p for p in prices if p > 0]
            
            if valid_prices:
                min_p = min(valid_prices)
                total_q = sum(a.get('quantity', 0) for a in item_auctions)
                extracted_records.append((time_str, item_id, min_p, total_q))

    return extracted_records

def toDB():
    init_db()
    os.makedirs(OLD_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Scan for JSON files
    files = [f for f in os.listdir(JSON_DIR) if f.endswith('.json')]
    
    if not files:
        print("No new JSON files to process.")
        return

    print(f"Found {len(files)} new files. Starting processing...")

    processed_count = 0
    for f_name in files:
        full_path = os.path.join(JSON_DIR, f_name)
        dest_path = os.path.join(OLD_DIR, f_name)
        
        records = process_json(full_path)
        
        if records:
            c.executemany("INSERT INTO price_history VALUES (?,?,?,?)", records)
            conn.commit()
            
            try:
                shutil.move(full_path, dest_path)
                print(f"Processed: {f_name}")
                processed_count += 1
            except Exception as e:
                print(f"Error moving file {f_name}: {e}")
        else:
            # Even if no watchlist items found, move file to 'old' to keep directory clean
            try:
                shutil.move(full_path, dest_path)
                print(f"Skipped: {f_name} (No matching items)")
            except Exception as e:
                print(f"Error moving file {f_name}: {e}")

    conn.close()
    print(f"Processing finished. Total files processed: {processed_count}")

if __name__ == "__main__":
    toDB()