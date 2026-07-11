import streamlit as st
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
def load_data():
  db_url = st.secrets["DATABASE_URL"]
  if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

  engine = create_engine(db_url)

  df = pd.read_sql("SELECT * FROM assets", engine) 

  return df


