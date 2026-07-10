import yfinance as yf
import time
import sqlite3
import pandas as pd

def update_prices():
  print("Initiating market sync...")

  conn = sqlite3.connect('portfolio.db')
  cursor = conn.cursor()
  df = pd.read_sql_query("SELECT id, ticker FROM assets where ticker is NOT NULL", conn)
  for index, row in df.iterrows():
    ticker_symbol = row['ticker']

    try:
      ticker = yf.Ticker(ticker_symbol)
      current_price = ticker.fast_info['last_price']

      cursor.execute('''
        UPDATE assets
        SET last_traded_price = ?
        WHERE id = ?
      ''',(current_price, row['id']))

      print(f"Updated {ticker_symbol} to ₹{round(current_price, 2)}")

      time.sleep(1)

    except Exception as e:
      print(f" Failed to update {ticker_symbol}. Error:{e}")

  conn.commit()
  conn.close()
  print("Market sync complete.")

if __name__ == "__main__":
  update_prices()
