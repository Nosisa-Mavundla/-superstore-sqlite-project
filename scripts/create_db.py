import sqlite3

conn = sqlite3.connect("database/superstore.db")
cursor = conn.cursor()
print("Database created successfuly!")
conn.close()