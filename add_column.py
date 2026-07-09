import sqlite3

def add_ticker_column():
  conn = sqlite3.connect('portfolio.db')
  cursor = conn.cursor()

  try:
    cursor.execute("ALTER TABLE assets ADD COLUMN ticker TEXT")
    print("Successfully added 'ticker' column to the vault.")
  except Exception as e:
    print(f"Error: {e}")

  conn.commit()
  conn.close()

if __name__=="__main__":
  add_ticker_column()
