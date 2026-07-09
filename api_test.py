import yfinance as yf
import streamlit as st

st.markdown("---")
st.subheader("Live Api Test")

try:
  ticker = yf.Ticker("TATASTEEL.NS")
  current_price = ticker.fast_info['last_price']

  st.success(f"Success, Python directly pulled the live data for Tata Steel: ₹{round(current_price,2)}")

except Exception as e:
  st.error(f"API Connection failed: {e}")                              
