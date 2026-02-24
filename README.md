# Gobli - WoW Auction House Tracker

Simple automated system to track and analyze World of Warcraft market trends using a Raspberry Pi and Python.

## Project Status
- [x] **Data Collection**: Scraper downloads snapshots from Blizzard API.
- [x] **Data Refining**: Moving raw JSON data into a structured SQLite database.
- [ ] **Visualization**: Generating price and quantity charts via Matplotlib.
- [ ] **AI Analysis**: Implementing AI to predict future market trends.
- [ ] **Notifications**: Discord alerts for price drops (Bargain Hunter).
- [ ] **Web Dashboard**: View your data in a browser instead of local charts.

## How it works
1. **Scraper** fetches a massive JSON file from Blizzard.
2. **Refinery** extracts only the items we want (Watchlist) and saves them to `wow_market.db`.
3. **Archive** moves used files to `archive/old` to keep the system fast and clean.
4. **Visualizer** draws charts so you can see when to buy or sell.

## Quick Start

1. **Setup:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install requests pandas matplotlib