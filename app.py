import streamlit as st
import pandas as pd

#1. Page Configuration (Makes it look clean and widescreen)
st.set_page_config(page_title="AI Portfolio Dashboard", layout="wide", initial_sidebar_state="expanded")

#2. Main Title
st.title("AI Quantitative Portfolio Analyst")
st.markdown("---")

#3. Connect to your Live Data
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSTUEBKe4VMr2NyAhlfw4uzeX2GIbbC8Tu_aUEGmHtpOxRmxE7Re_uxVu_0BB2vY_xcwwDWfRpmJkCV/pub?gid=0&single=true&output=csv"

@st.cache_data(ttl=60) # This refreshes the data every 60 seconds
def load_data():
  try:
    data = pd.read_csv(CSV_URL)
    return data
  except Exception as e:
    st.error(f"Error loading this data: {e}")
    return None

df = load_data()

#4. Render the Data
if df is not None:
  st.subheader("Live Portfolio Analytics")
  #Displays your entire sheet beautifully
  st.dataframe(df, use_container_width=True, hide_index=True)
else:
  st.info("Waiting for data stream... Make sure your google Sheet link is pasted correctly above")
