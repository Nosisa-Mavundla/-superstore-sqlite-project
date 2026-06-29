import streamlit as st
import sqlite3 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("data/superstore.csv")

#create database connection
conn = sqlite3.connect(r"database/superstore.db")
cursor= conn.cursor()

#page config
st.set_page_config(page_title="Superstore Dashboard", layout= "wide")
st.title("Superstore Sales Dashboard")
st.markdown("___")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page",[
        "Executive Summary",
          "Business Performance",
            "Diagnostic Analysis", 
            "Trend Analysis"]
            )


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

#Total regions
query= """
SELECT (SUM(Sales)/COUNT(DISTINCT "Order ID"))AS AOV
FROM superstore;
"""
cursor.execute(query)
AOV= cursor.fetchone()[0]

#Total Sales by region 
query = """
SELECT Region, SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY Region
ORDER BY Total_Sales DESC
"""

df_Region = pd.read_sql_query(query, conn)

fig1 = px.bar(
    df_Region,
    x ="Region",
    y= "Total_Sales",
    title= "Sales by Region"
)
fig1.update_traces(
    hovertemplate="Sales:$%{y:,.2f}<br>Region: %{x}<extra></extra>"
)

# Sales by Category
query = """
SELECT Category, SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY Category
ORDER BY Total_Sales DESC
"""

df_Category =pd.read_sql_query(query, conn)

fig2 = px.pie(
    df_Category,
    values= "Total_Sales",
    names ="Category",
    title = "Sales by Category",
    hole=0.4
)
fig2.update_traces(
    hovertemplate="Category: %{label}<br>Sales:$ %{value:,.2f}<br>%{percent}<extra></extra>"
)

fig2.update_traces(
    textposition="inside",
    textinfo="percent+label")

#Sales trend over time
#Sales by year
query = """
SELECT 
    strftime('%Y', [Order Date]) AS Year,
    SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY Year
ORDER BY Year;
"""

df_Year = pd.read_sql_query(query, conn)

fig3 = px.line(
    df_Year,
    x="Year",
    y="Total_Sales",
    title="Sales by Year",
    markers=True
)
fig3.update_xaxes(type="category")
fig3.update_traces(
    hovertemplate="Sales:$ %{y:,.2f}<br>Year: %{x}<extra></extra>"
)


#Total Sales by region 
query = """
SELECT Region, SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY Region
ORDER BY Total_Sales DESC
"""

df_Region = pd.read_sql_query(query, conn)

fig5 = px.bar(
    df_Region,
    x ="Region",
    y= "Total_Sales",
    height= 500,
    width= 100,
    title= "Sales by Region"
    
)
fig5.update_traces(
    hovertemplate="Sales:$%{y:,.2f}<br>Region: %{x}<extra></extra>"
)

if page == "Executive Summary":
    st.title("Executive Summary")
#KPI Container to look like bi dash
    kpi_container = st.container()

    with kpi_container:
      col1, col2, col3, col4 = st.columns(4)

      col1.metric("Total Sales", value=f"${Total_Sales:,.2f}")
      col2.metric("Total Orders",value= f"{Total_Orders:,}")
      col3.metric("Total Customers", value=f"{Total_Customers:,}")
      col4.metric("Average Order Value", value=f"${AOV:,.2f}")

    c_container = st.container()
    with c_container:
      col1, col2, col3= st.columns(3)

      col1.plotly_chart(fig1, use_container_width=True)
      col2.plotly_chart(fig2, use_container_width=True)
      col3.plotly_chart(fig3, use_container_width=True)
    
    
elif page == "Business Performance":
      
    st.title("Business Performance")
    st.subheader("Overall Performance")

    ci_container = st.container()

    with ci_container:
      col1,  = st.columns(1)

      col1.plotly_chart(fig5,)
      

    st.subheader("Product Performance")

    ci_container = st.container()

    with ci_container:
      col1, col2, col3 = st.columns(3)

      col1.plotly_chart(fig2, use_container_width=True)
  #Finish up with salesby sub categoryan salesby 10 top performing proucts/write code for both fromscratch





