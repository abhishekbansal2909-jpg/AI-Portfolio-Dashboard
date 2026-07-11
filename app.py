import streamlit as st
import pandas as pd
from data_manager import load_data
from ui_components import color_verdict, display_chart

#1. Page Configuration (Makes it look clean and widescreen)
st.set_page_config(page_title="AI Portfolio Dashboard", layout="wide", initial_sidebar_state="expanded")

import sqlite3

#UI Expansion form
st.sidebar.header("Add New Asset")
with st.sidebar.form("add_stock_form", clear_on_submit = True):
  new_company = st.text_input("Company Name (e.g., Infosys)")
  new_ticker = st.text_input("Yahoo Finance Ticker (e.g., INFY.NS)")
  new_analysis = st.selectbox("Analysis Type", ["Fundamental", "Technical"])
  add_submit = st.form_submit_button("Add to Vault")

  if add_submit and new_company and new_ticker:
    try:
      conn = sqlite3.connect('portfolio.db')
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM assets LIMIT 0")
      db_columns = [desc[0] for desc in cursor.description]
      st.sidebar.write(db_columns)
      exact_company_col = [col for col in db_columns if "Company" in col][0]
      exact_analysis_col = [col for col in db_columns if "Analysis" in col][0]
      query = f'INSERT INTO assets ("{exact_company_col}", "ticker", "{exact_analysis_col}") VALUES (?, ?, ?)'
      cursor.execute(query, (new_company, new_ticker.upper(), new_analysis))
 
      conn.commit()
      conn.close()

      st.sidebar.success(f"Successfully added {new_ticker}!")
      st.rerun() 

    except Exception as e:
      st.sidebar.error(f"Database error: {e}")

#2. Main Title
st.title("AI Quantitative Portfolio Analyst")
st.markdown("---")

#3. Connect to your Live Data
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSTUEBKe4VMr2NyAhlfw4uzeX2GIbbC8Tu_aUEGmHtpOxRmxE7Re_uxVu_0BB2vY_xcwwDWfRpmJkCV/pub?gid=0&single=true&output=csv"

df = load_data()

#4. Render the Data
if df is not None:
  st.subheader("Live Portfolio Analytics")

  #Interactive Filter Section
  st.subheader("Asset Search")

  # Create a unique list of companies, adding an "All Assets" option at the front
  company_list = ["All Assets"] + df['Company Name'].str.strip().unique().tolist()

  # Generates the drop down menu
  selected_company = st.selectbox("Select a company to analyze:", company_list)
  
  # Filter the data based on the uesr's selection
  if selected_company != "All Assets":
    df = df[df['Company Name'].str.strip() == selected_company]
  
  st.markdown("---")
  

  #--KPI Cards Section---
  st.subheader("Portfolio Health Check")
  col1, col2, col3 = st.columns(3)

  with col1:
    total_assets = len(df)
    st.metric(label="Total Assets Monitored", value= total_assets)

  with col2:
    #Assuming your column is named exactly "Analysis Type"
    fundamental_count = len(df[df['Analysis Type'].str.strip() == 'Fundamental'])
    st.metric(label="Fundamental Setups",value = fundamental_count)

  with col3:
    technical_count = len(df[df['Analysis Type'].str.strip() == 'Technical'])
    st.metric(label="Technical Setups",value = technical_count)

  st.markdown("---") #adds a clean dividing line before the table

  #----------------------

  display_chart(df)

  # Add this line here to sort the data(change "confidence Score" to match your exact google sheet column name)
  df=df.sort_values(by="Confidence Score", ascending = False)
  
  df['Last Traded Price'] = df['Last Traded Price'].apply(lambda x : f"₹{float(x):,.2f}" if pd.notnull(x) else x)
  df = df.drop(columns=['ticker'], errors = 'ignore')
  
  styled_df = df.style.map(color_verdict, subset = ['AI Verdict'])

  st.write(df.columns.tolist())
  
  #Displays your entire sheet beautifully
  st.dataframe(styled_df, use_container_width=True, hide_index=True,
              column_config={
                "Confidence Score": st.column_config.ProgressColumn(
                  "AI Conviction Score",
                  help= "Gemini's 1-10 Confidence Rating",
                  format="%d",
                  min_value=0,
                  max_value=10,),
              "Current price":st.column_config.NumberColumn(
                "Last Traded Price",
                format="₹%.2f"),
                "AI Verdict": st.column_config.TextColumn(
                  "AI Strategic Analysis",
                  width="large")
              }
                )
else:
  st.info("Waiting for data stream... Make sure your google Sheet link is pasted correctly above")

