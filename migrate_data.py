import pandas as pd
import sqlite3

sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSTUEBKe4VMr2NyAhlfw4uzeX2GIbbC8Tu_aUEGmHtpOxRmxE7Re_uxVu_0BB2vY_xcwwDWfRpmJkCV/pub?gid=0&single=true&output=csv"

CSV_URL = sheet_url.replace('edit?usp=sharing', '/export?format=csv')
df = pd.read_csv(CSV_URL)
df.columns = df.columns.str.strip()

df['Company Name'] = df['Company Name'].str.strip()
df['Analysis Type'] = df['Analysis Type'].str.strip()

conn = sqlite3.connect('portfolio.db')
cursor = conn.cursor()

for index, row in df.iterrows():
  # question marks are acting as placeholders
  cursor.execute('''
    INSERT INTO assets (company_name, analysis_type, last_traded_price, ai_verdict, confidence_score)
    VALUES (?,?,?,?,?) 
  ''',(
    row['Company Name'],
    row['Analysis Type'],
    row['Last Traded Price'],
    row['AI Strategic Analysis'],
    row['Confidence Score']

  ))

# Save the changes and lock the vault
conn.commit()
conn.close()

print("Migration Complete and all spreadsheet data is locked in the vault")
