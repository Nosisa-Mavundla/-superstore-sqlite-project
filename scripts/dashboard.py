import streamlit as st
import sqlite3 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("data/superstore.csv")
#page config
st.set_page_config(page_title="Superstore Dashboard", layout= "wide")
st.title("Superstore Sales Dashboard")
st.markdown("___")

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

#Total regions
query= """
SELECT COUNT (DISTINCT Region)
FROM superstore;
"""
cursor.execute(query)
Total_Regions = cursor.fetchone()[0]

#KPI Container to look like bi dash
kpi_container = st.container()

with kpi_container:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", value=f"${Total_Sales:,.2f}")
    col2.metric("Total Orders",value= f"{Total_Orders:,}")
    col3.metric("Total Customers", value=f"{Total_Customers:,}")
    col4.metric("Total Regions", value=f"{Total_Regions:,}")

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


#Sales by Customer Segments

query = """
SELECT Segment, SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY Segment
ORDER BY Total_Sales DESC
"""
df_Segment = pd.read_sql_query(query, conn)

fig3 = px.bar(
    df_Segment,
    x= "Segment",
    y = "Total_Sales",
    title = "Sales by Segment"
)
fig3.update_traces(
    hovertemplate="Sales: $%{y:,.2f}<br>Segment: %{x}<extra></extra>"
)
#Top 10 high performing cities
query = """
SELECT City, SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY City
ORDER BY Total_Sales DESC
LIMIT 10
"""

df_City = pd.read_sql_query(query, conn)

fig4 = px.bar(
    df_City,
    y= "City",
    x="Total_Sales",
    title="Top 10 high performing cities",
    orientation="h"#horizontal bar chart
)
fig4.update_layout(
    yaxis={"categoryorder": "total ascending"}#This puts the highest sales cities at the top
)
fig4.update_traces(
    hovertemplate="City: %{y}<br>Sales:$ %{x:,.2f}<extra></extra>"
)


#container for bar graphs
c_container = st.container()
with c_container:
    col1, col2, col3, col4= st.columns(4)

    col1.plotly_chart(fig1, use_container_width=True)
    col2.plotly_chart(fig2, use_container_width=True)
    col3.plotly_chart(fig3, use_container_width=True)
    col4.plotly_chart(fig4, use_container_width=True)

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

fig5 = px.line(
    df_Year,
    x="Year",
    y="Total_Sales",
    title="Sales by Year",
    markers=True
)
fig5.update_xaxes(type="category")
fig5.update_traces(
    hovertemplate="Sales:$ %{y:,.2f}<br>Year: %{x}<extra></extra>"
)

#sales by month
#monthly sales trend
query = """
SELECT 
    strftime('%m', [Order Date]) AS Month,
    SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY Month
ORDER BY Month;
"""

df_Month = pd.read_sql_query(query, conn)

fig6= px.line(
    df_Month,
    x="Month",
    y="Total_Sales",
    title="Sales by Months across all years",
    markers=True
)
fig6.update_xaxes(type="category")
fig6.update_traces(
    hovertemplate="Month: %{x}<br>Sales:$ %{y:,.2f}<extra></extra>"
)

#Each region with its total unique orders
query = """
SELECT Region, COUNT(DISTINCT "Order ID") AS Total_Orders
FROM superstore
GROUP BY Region
ORDER BY Total_Orders DESC
"""

df_Orders = pd.read_sql_query(query, conn)

fig7= px.bar(
    df_Orders,
    x ="Region",
    y= "Total_Orders",
    title= "Orders by Region"
)
fig7.update_traces(
    hovertemplate="Orders:%{y:}<br>Region: %{x}<extra></extra>"
)

#Sales by categories in each region
query = """
SELECT Region, Category,SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY Region, Category
ORDER BY Region, Total_Sales
"""

df_reg_cat = pd.read_sql_query(query, conn)

fig8 = px.bar(
    df_reg_cat,
    x= "Region",
    y="Total_Sales",
    color= "Category",
    barmode= "group",
    title="Region Sales by each product mix"
)
fig8.update_traces(
     hovertemplate="Total_Sales:$%{y:,.2f}<br>Region: %{x}<extra></extra>"
)


#container for line charts
c_container = st.container()
with c_container:
    col1, col2, col3 , col4= st.columns(4)

    col1.plotly_chart(fig5, use_container_width=True)
    col2.plotly_chart(fig6,use_container_width=True)
    col3.plotly_chart(fig7, use_container_width=True)
    col4.plotly_chart(fig8, use_container_width=True)

#Average Order Value: customers spending per order
query = """
SELECT Region,
       (SUM(Sales)/COUNT(DISTINCT "Order ID")) AS AOV
FROM superstore
GROUP BY Region
ORDER BY AOV
"""

df_aov = pd.read_sql_query(query, conn)
df_aov = df_aov.sort_values("AOV")

fig9 = go.Figure()

# STEMS (from baseline 0 to value)
df_aov = pd.read_sql_query(query, conn)
df_aov = df_aov.sort_values("AOV")

fig9 = go.Figure()

# ✔ STEMS (baseline 0 → value)
for _, row in df_aov.iterrows():
    fig9.add_trace(
        go.Scatter(
            x=[row["Region"], row["Region"]],
            y=[0, row["AOV"]],
            mode="lines",
            line=dict(color="lightgray", width=2),
            showlegend=False
        )
    )

# ✔ HEADS (lollipops)
fig9.add_trace(
    go.Scatter(
        x=df_aov["Region"],
        y=df_aov["AOV"],
        mode="markers",
        marker=dict(size=12, color="steelblue"),
        hovertemplate="AOV: %{y:,.2f}<br>Region: %{x}<extra></extra>"
    )
)

fig9.update_layout(
    title="Average Order Value by Region",
    xaxis_title="Region",
    yaxis_title="AOV"
)

st.plotly_chart(fig9)







