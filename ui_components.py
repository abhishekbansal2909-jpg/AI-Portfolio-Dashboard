import streamlit as st

def color_verdict(val):
    val_str = str(val).lower()
    if 'bullish' in val_str:
      return 'color: #00FF00' #Bright Green
    elif 'bearish' in val_str:
      return 'color: #FF4B4B' #bright red
    return ''

def display_chart(df):
  st.subheader("Portfolio Conviction Breakdown")
  st.bar_chart(df, x="Company Name", y="Confidence Score")
  st.markdown("---")
