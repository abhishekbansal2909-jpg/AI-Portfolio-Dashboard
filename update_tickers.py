import sqlite3

def populate_tickers():
  print("Mapping company names to Yahoo finance tickers...")
  conn = sqlite3.connect('portfolio.db')
  cursor = conn.cursor()

  ticker_map = {
    'Tata steel': 'TATASTEEL.NS',
    'Adani Power': 'ADANIPOWER.NS',
    'Coal India': 'COALINDIA.NS',
    'Larsen and Toubro': 'LT.NS',
    'HDFC Bank': 'HDFCBANK.NS',
    'Adani Ports': 'ADANIPORTS.NS',
    'NTPC':'NTPC.NS',
    'Container Corporation of India': 'CONCOR.NS',
    'Adani Enterprises': 'ADANIENT.NS',
    'Reliance': 'RELIANCE.NS',
    'JSW Infrastructure': 'JSWINFRA.NS',
    'Rail Vikas Nigam Ltd': 'RVNL.NS',
    'Dredging Corporation of India': 'DREDGECORP.NS'
  }

  try:
    for company, ticker in ticker_map.items():
      cursor.execute('''
        UPDATE assets
        SET ticker = ?
        WHERE company_name = ?
      ''',(ticker, company))
    print("Ticker Column Successfully populated")

  except Exception as e:
    print(f"Error: [e]")

  conn.commit()
  conn.close()

if __name__ == "__main__":
  populate_tickers()

  
