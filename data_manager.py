import streamlit as st
import pandas as pd

@st.cache_data(ttl=60)
def load_and_clean_data(sheet_url):
  try:
    csv_url = sheet_url.replace('/edit?usp=sharing','/export?format=csv')
    df = pd.read_csv(csv_url)

    df['Company Name'] = df['Company Name'].str.strip()
    df['Analysis Type'] = df['Analysis Type'].str.strip()

    return df

  except Exception as e:
    st.error(f"Error loading the database: {e}")
    return None
