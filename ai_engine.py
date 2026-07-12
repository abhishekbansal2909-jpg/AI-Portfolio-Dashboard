import os
import time
import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine, text
import google.generativeai as genai

def get_rsi(ticker_symbol):
  """Calculates 14-DAY RSI using pure pandas"""
  try:
    data: = yf.download(ticker_symbol, period="1mo", progress = False)
    if len(data) < 15:
      return "N/A"
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain/loss
    rsi = 100 - (100/(1+ rs))
    return round(rsi.iloc[-1].item(),2)
  except Exception:
    return "N/A"

def run_ai_analysis():
  print("Waking up Gemini AI engine....")
  db_url = os.environ.get("DATABASE_URL")
  if db_url and db_url.startswith(:postgres://"):
    db_url = db_url.replace(postgres://", "postgresql://",1)
  engine = create_engine(db_url)

  genai.configure(api_key = os.environ.get("GEMINI_API_KEY"))
  model = genai.GenerativeModel('gemini-1.5-flash')

  query = """
    SELECT id, ticker, company_name
    FROM assets
    WHERE ticker is NOT NULL
    AND (ai_strategic_analysis is NULL OR confidence_score IS NULL)
  """

  df = pd.read_sql_query(query, engine)

  if df.empty:
    print("All assets have been analyzed, AI returning to sleep.")
    return

  with engine.begin() as conn:
    for index, row in df.iterrows():
      ticker_sym = row['ticker']
      company = row['company_name']
      print(f"Analyzing {ticker_sym}...")

      try:
        # fetching live data for the prompt
        ticker = yf.Ticker(ticker_sym)
        info = ticker.info
        fast_info = ticker.fast_info

        pe_ratio = info.get('trailingPE', info.get('forwardPE', 'N/A'))
        market_cap = fast_info.get('market_cap', 'N/A')
