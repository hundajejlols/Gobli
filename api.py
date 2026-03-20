from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI(title="Gobli API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
DB_NAME = "wow_market.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    return conn

@app.on_event("startup")
def startup_event():
    print("Starting Gobli API server...")

@app.get("/")
def read_root():
    return {"status": "API is running"}

@app.get("/api/items")
def get_tracked_items():
    """Zwraca liste unikalnych ID przedmiotow z bazy."""
    conn = get_db_connection()
    try:
        items = conn.execute("SELECT DISTINCT item_id FROM price_history").fetchall()
        return {"tracked_items": [item["item_id"] for item in items]}
    finally:
        conn.close()

@app.get("/api/items/{item_id}/history")
def get_item_history(item_id: int, limit: int = 50):
    conn = get_db_connection()
    try:
        # Uzywamy GROUP BY timestamp, aby wyeliminowac duplikaty pobierane z bazy
        query = """
            SELECT timestamp, MIN(min_price) as min_price, MAX(quantity) as quantity 
            FROM price_history 
            WHERE item_id = ? 
            GROUP BY timestamp
            ORDER BY timestamp DESC 
            LIMIT ?
        """
        rows = conn.execute(query, (item_id, limit)).fetchall()
        
        if not rows:
            print("No data found for the requested item.")
            raise HTTPException(status_code=404, detail="Item data not found")
            
        return {
            "item_id": item_id,
            "history": [dict(row) for row in rows]
        }
    finally:
        conn.close()