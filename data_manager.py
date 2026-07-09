import streamlit as st
import pandas as pd
import sqlite3

def load_data():
  """Connects to the SQL lite, fetches data and format it for the UI."""

  conn = sqlite3.connect('portfolio.db')
  query = "SELECT * FROM assets"
  df = pd.read_sql_query(query, conn)
  conn.close()

  df = df.rename(columns={
    'company_name': 'Company Name',
    'analysis_type': 'Analysis Type',
    'last_traded_price': 'Last Traded Price',
    'ai_verdict': 'AI Verdict',
    'confidence_score':'Confidence Score'
  })

  if 'id' in df.columns:
    df = df.drop(columns=['id'])
  return df


