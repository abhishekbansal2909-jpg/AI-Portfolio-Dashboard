import sqlite3

#1 Connect to the database

conn = sqlite3.connect('portfolio.db')

#2 Create a cursor 

cursor = conn.cursor()

#Write the SQL command to build the table
cursor.execute('''
CREATE TABLE IF NOT EXISTS assets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  company_name TEXT NOT NULL,
  analysis_type TEXT,
  last_traded_price REAL,
  ai_verdict TEXT,
  confidence_score INTEGER
  )
''')

#4 Save the changes and close the vault
conn.commit()
conn.close()

print("Success: Database 'portfolio.db' and 'assets' table have been created!")
