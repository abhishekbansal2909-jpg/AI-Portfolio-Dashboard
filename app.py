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
  
  #Displays your entire sheet beautifully
  st.dataframe(df, use_container_width=True, hide_index=True,
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
