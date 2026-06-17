import sqlite3
import pandas as pd

df = pd.read_csv("data/superstore.csv")

#Fix data types
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)
df["Sales"] = pd.to_numeric(df["Sales"])
df["Postal Code"] = df["Postal Code"].astype(str).str.replace(".0", "", regex=False)

#Connect to the SQLITE DB
conn= sqlite3.connect("database/superstore.db")

#Load data into the table
df.to_sql("superstore", conn, if_exists="replace", index=False)

print("Data loaded into SQLite successfully")

conn.close()