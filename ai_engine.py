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
