import streamlit as st
import sqlite3 
import pandas as pd
df = pd.read_csv("data/superstore.csv")
#page config
st.set_page_config(page_title="Superstore Dashboard", layout= "wide")
st.title("Superstore Sales Dashboard")

#create database connection
conn = sqlite3.connect(r"database/superstore.db")
cursor= conn.cursor()

#Total Superstore Sales on the dashboard
query= """
SELECT SUM(Sales)
FROM superstore
"""

cursor.execute(query)
Total_Sales = cursor.fetchone()[0]

#Total Orders on the dashboard
query= """
SELECT COUNT( DISTINCT "Order ID") AS Total_Orders
FROM superstore
"""
cursor.execute(query)
Total_Orders = cursor.fetchone()[0]

#Total customers on the dashboard
query= """
SELECT COUNT( DISTINCT "Customer ID") AS Total_Customers
FROM superstore
"""
cursor.execute(query)
Total_Customers = cursor.fetchone()[0]

#KPI Container to look like bi dash
kpi_container = st.container()

with kpi_container:
    col1, col2, col3 = st.columns([2,1,2])

    col1.metric("Total Sales", value=f"${Total_Sales:,.2f}")
    col2.metric("Total Orders",value= f"{Total_Orders:,}")
    col3.metric("Total Customers", value=f"{Total_Customers:,}")