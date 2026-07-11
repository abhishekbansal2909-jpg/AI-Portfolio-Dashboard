import yfinance as yf
import time
import pandas as pd
import os
import sqlalchemy
from sqlalchemy import create_engine, text

def update_prices():
  print("Initiating market sync...")

  db_url = os.environ.get("DATABASE_URL")
  if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
  engine = create_engine(db_url)
  df = pd.read_sql_query("SELECT id, ticker FROM assets where ticker is NOT NULL", engine)
  
  with engine.begin() as conn:
    for index, row in df.iterrows():
      ticker_symbol = row['ticker']
  
      try:
        ticker = yf.Ticker(ticker_symbol)
        current_price = ticker.fast_info['last_price']
  
        query = text('''
          UPDATE assets
          SET last_traded_price = :price
          WHERE ticker = :ticker
        ''')
        conn.execute(query, {"price": current_price, "ticker": ticker_symbol})
        
        print(f"Updated {ticker_symbol} to ₹{round(current_price, 2)}")
  
        time.sleep(1)
  
      except Exception as e:
        print(f" Failed to update {ticker_symbol}. Error:{e}")

if __name__ == "__main__":
  update_prices()
