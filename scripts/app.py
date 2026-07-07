import streamlit as st
import sqlite3 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("data/superstore.csv")

#create database connection
conn = sqlite3.connect(r"database/superstore.db")
cursor= conn.cursor()

# Load the complete dataset once for dashboard filters
df = pd.read_sql_query("SELECT * FROM superstore", conn)

# Convert Order Date from text into a pandas datetime column
df["Order Date"] = pd.to_datetime(df["Order Date"])
#convert order date to year/month/monthname
df["Year"] = df["Order Date"].dt.year
df["Month_Number"] = df["Order Date"].dt.month
df["Month"] = df["Order Date"].dt.month_name()

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


st.sidebar.header("Dashboard Filters")

selected_regions = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

selected_segments = st.sidebar.multiselect(
    "Segment",
    options=sorted(df["Segment"].dropna().unique()),
    default=sorted(df["Segment"].dropna().unique())
)

selected_categories = st.sidebar.multiselect(
    "Category",
    options=sorted(df["Category"].dropna().unique()),
    default=sorted(df["Category"].dropna().unique())
)

selected_years = st.sidebar.multiselect(
    "Year",
    options=sorted(df["Order Date"].dt.year.dropna().unique()),
    default=sorted(df["Order Date"].dt.year.dropna().unique())
)
# Keep only rows that match the sidebar selections
df_filtered = df[
    (df["Region"].isin(selected_regions)) &
    (df["Segment"].isin(selected_segments)) &
    (df["Category"].isin(selected_categories)) &
    (df["Order Date"].dt.year.isin(selected_years))
]

st.sidebar.write("Filtered rows:", len(df_filtered))

# Download the full dataset
full_data_csv = df.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    label="Download Full Data (CSV)",
    data=full_data_csv,
    file_name="superstore_full_data.csv",
    mime="text/csv"
)

# Download data matching the active filters
filtered_data_csv = df_filtered.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    label="Download Filtered Data (CSV)",
    data=filtered_data_csv,
    file_name="superstore_filtered_data.csv",
    mime="text/csv"
)





if page == "Executive Summary":
    st.title("Executive Summary")
#KPI Container to look like bi dash
    
#Total Superstore Sales on the dashboard
    
    Total_Sales = df_filtered["Sales"].sum()

#Total Orders on the dashboard
    Total_Orders = df_filtered["Order ID"].nunique()

#Total customers on the dashboard
    Total_Customers = df_filtered["Customer ID"].nunique()
#AOV
    AOV = Total_Sales / Total_Orders if Total_Orders != 0 else 0

    kpi_container = st.container()

    with kpi_container:
      col1, col2, col3, col4 = st.columns(4)

      col1.metric("Total Sales", value=f"${Total_Sales:,.2f}")
      col2.metric("Total Orders",value= f"{Total_Orders:,}")
      col3.metric("Total Customers", value=f"{Total_Customers:,}")
      col4.metric("Average Order Value", value=f"${AOV:,.2f}")

#Total Sales by region 
   # Sales by Region — based on sidebar filters
    df_Region = (
    df_filtered
    .groupby("Region", as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "Total_Sales"})
    .sort_values("Total_Sales", ascending=False)
)

    fig1 = px.bar(
    df_Region,
    x="Region",
    y="Total_Sales",
    title="Sales by Region"
)

    fig1.update_traces(
    hovertemplate="Sales: $%{y:,.2f}<br>Region: %{x}<extra></extra>"
)

# Sales by Category — based on sidebar filters
    df_Category = (
    df_filtered
    .groupby("Category", as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "Total_Sales"})
    .sort_values("Total_Sales", ascending=False)
)

    fig2 = px.pie(
    df_Category,
    values="Total_Sales",
    names="Category",
    title="Sales by Category",
    hole=0.4
)

    fig2.update_traces(
    hovertemplate="Category: %{label}<br>Sales: $%{value:,.2f}<br>%{percent}<extra></extra>",
    textposition="inside",
    textinfo="percent+label"
)

#Sales trend over time
#Sales by year

    df_Year = (
    df_filtered
    .groupby("Year", as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "Total_Sales"})
    .sort_values("Year")
)


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
    
    c_container = st.container()
    with c_container:
      col1, col2, col3= st.columns(3)

      col1.plotly_chart(fig1, use_container_width=True)
      col2.plotly_chart(fig2, use_container_width=True)
      col3.plotly_chart(fig3, use_container_width=True)
    
    
elif page == "Business Performance":
      
    st.title("Business Performance")
    st.subheader("Overall Performance")
#Total Sales by region 
   # Sales by Region — based on sidebar filters
    df_Region = (
    df_filtered
    .groupby("Region", as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "Total_Sales"})
    .sort_values("Total_Sales", ascending=False)
)

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
    ci_container = st.container()

    with ci_container:
      col1,  = st.columns(1)

      col1.plotly_chart(fig5,)

    st.subheader("Product Performance")
    #Sales by category
    df_Category = (
    df_filtered
    .groupby("Category", as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "Total_Sales"})
    .sort_values("Total_Sales", ascending=False)
)

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

#Sales by sub-category
    df_subcategory = (
    df_filtered
    .groupby("Sub-Category", as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "Total_Sales"})
    .sort_values("Total_Sales", ascending=False)
)
    fig6= px.bar(
    df_subcategory,
     x="Total_Sales",
     y= "Sub-Category",
     orientation= "h",
     title= "Sales by Sub-Category"
)
    fig6.update_layout(
    yaxis = {"categoryorder": "total ascending"}
)
    fig6.update_traces(
    hovertemplate="Sub-Category: %{y}<br>Sales:$ %{x:,.2f}<extra></extra>"

)

#Top 10 high performing products
    df_productname = (
    df_filtered
    .groupby("Product Name", as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "Total_Sales"})
    .sort_values("Total_Sales", ascending=False)
    .head(10)
)

    fig7 = px.bar(
    df_productname,
    x = "Total_Sales",
    y = "Product Name",
    orientation= "h",
    title= "Top 10 high perfroming products"
)
    fig7.update_layout(
    yaxis = {"categoryorder": "total ascending"}
)
    fig7.update_traces(
    hovertemplate="Product Name: %{y}<br>Sales:$ %{x:,.2f}<extra></extra>"
)
    ci_container = st.container()

    with ci_container:
      col1, col2, col3 = st.columns(3)

      col1.plotly_chart(fig2, use_container_width=True)
      col2.plotly_chart(fig6, use_container_width=True)
      col3.plotly_chart(fig7, use_container_width=True)


      st.subheader("Customer and Market Performance")
#Sales by segment
    df_segment = (
    df_filtered
    .groupby("Segment", as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "Total_Sales"})
    .sort_values("Total_Sales", ascending=False)
)

    fig8 = px.treemap(
    df_segment,
    path=["Segment"],
    values="Total_Sales",
    title="Sales by Segment"
)
    fig8.update_traces(
    hovertemplate="Segment: %{label}<br>Sales:$ %{value:,.2f}<br> Share: %{percentRoot:.1%}<extra></extra>"
)
    fig8.update_traces(
    textinfo= "label+percent root"
)

#Top 10 high performing cities
    df_city = (
    df_filtered
    .groupby("City", as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "Total_Sales"})
    .sort_values("Total_Sales", ascending=False)
    .head(10)
)
    fig9= px.bar(
    df_city,
    x="Total_Sales",
    y="City",
    orientation="h",
    title="Top 10 high performing cities"
)
    fig9.update_layout(
    yaxis={"categoryorder" : "total ascending"}
)
    fig9.update_traces(
    hovertemplate="City: %{y}<br>Sales:$ %{x:,.2f}<extra></extra>"
)


    ci_container = st.container()

    with ci_container:
      col1, col2 =st.columns(2)
      col1.plotly_chart(fig8, use_container_width=True)
      col2.plotly_chart(fig9, use_container_width=True)


elif page == "Diagnostic Analysis":
  st.title("Diagnostic Analysis") 
  st.markdown("### Why is the South Region Underperforming")

  st.markdown("""
               <h2 style= "font-size:20px;">
               Evidence 1:Regional Order Volume
               </h2>
               """, unsafe_allow_html=True)

#Regional Order Volume/ total orders by region

  df_rov = (
    df_filtered
    .groupby("Region", as_index=False)["Order ID"]
    .nunique()
    .rename(columns={"Order ID": "Total_Orders"})
    .sort_values("Total_Orders", ascending=False)
)


  fig10 = px.bar(
     df_rov,
     x= "Total_Orders",
     y="Region",
     orientation="h",
     title="Total Orders by Region"
)
  fig10.update_layout(
     yaxis={"categoryorder": "total ascending"}
)

  st.plotly_chart(fig10)
  st.markdown("""
        <p style="font-size:18px;">
        South recorded the lowest number of orders among all regions, indicating that lower customer activity is a major contributor to its weaker sales performance.

        </p>
        """, unsafe_allow_html=True)
#category performance by region/Product category performance/is south's underperformance driven by product category's low performance, is underperfomance driven by  single category or all categories.
  
  st.markdown("""
               <h2 style="font-size:20px;">
               Evidence 2: Category Performance
               </h2>
               """, unsafe_allow_html=True)
  df_rpcp = (
    df_filtered
    .groupby(["Region", "Category"], as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "Total_Sales"})
)

  fig11 = px.bar(
   df_rpcp,
   x="Region",
   y="Total_Sales",
   color= "Category",
   barmode="group",
   title="Category Performance by Region"
)

  fig11.update_traces(
     hovertemplate="Total_Sales:$%{y:,.2f}<br>Region: %{x}<extra></extra>"
)
  st.plotly_chart(fig11)

  
  st.markdown("""
              <p style="font-size:18px;"> 
               Every product category generated the lowest sales in the South, indicating that the underperformance is widespread rather than concentrated in a single category.
              </p>
               """,unsafe_allow_html=True)
  

#AOV/Average order value by region
  st.markdown("""
<h2 style="font-size:20px;">
Evidence 3: Average Order Value
</h2>
""", unsafe_allow_html=True)
  # Average Order Value by Region
  df_aov = (
    df_filtered
    .groupby("Region", as_index=False)
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Orders=("Order ID", "nunique")
    )
)

  df_aov["AOV"] = df_aov["Total_Sales"] / df_aov["Total_Orders"]
  df_aov = df_aov.sort_values("AOV")

  fig12 = go.Figure()

# STEMS
  for _, row in df_aov.iterrows():
    fig12.add_trace(
        go.Scatter(
            x=[row["Region"], row["Region"]],
            y=[0, row["AOV"]],
            mode="lines",
            line=dict(color="lightgray", width=2),
            showlegend=False
        )
    )

# HEADS
    fig12.add_trace(
    go.Scatter(
        x=df_aov["Region"],
        y=df_aov["AOV"],
        mode="markers",
        marker=dict(size=12, color="steelblue"),
        hovertemplate="AOV: %{y:,.2f}<br>Region: %{x}<extra></extra>",
        showlegend=False
    )
)
 
    fig12.update_layout(
    title="Average Order Value by Region",
    xaxis_title="Region",
    yaxis_title="AOV"
)

  st.plotly_chart(fig12, use_container_width=True)

  st.markdown("""
<p style="font-size:18px;">
Although South underperforms in total sales, its Average Order Value exceeds
that of West and Central. This suggests that order value is not the primary
driver of South's weaker sales performance.
</p>
""", unsafe_allow_html=True)

  st.markdown("""
<p style="font-size:18px;">
<strong>Overall Diagnostic Summary:</strong>
South's underperformance is primarily driven by lower order volume. The consistently low sales across all product categories are a consequence of fewer customer transactions, while Average Order Value indicates that customers spend competitive amounts when they do make purchases.
</p>
""", unsafe_allow_html=True)
    

elif page=="Trend Analysis":
   st.title("Trend Analysis")

   st.markdown(""" 
               <p style =" font-size: 20px;">
               How has the business performance changed overtime?
               </p>""", unsafe_allow_html=True)

#Sales by years/ is the business growing over the years
   df_Year = (
    df_filtered
    .groupby("Year", as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "Total_Sales"})
    .sort_values("Year")
)

   fig13 = px.line(
    df_Year,
    x="Year",
    y="Total_Sales",
    title="Sales by Year",
    markers=True
)
   fig13.update_xaxes(type="category")
   fig13.update_traces(
    hovertemplate="Sales:$ %{y:,.2f}<br>Year: %{x}<extra></extra>"
)
   
   st.plotly_chart(fig13)
   #Monthly sales across all regions
   df_monthly_sales = (
    df_filtered
    .groupby(["Month_Number", "Month"], as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "Total_Sales"})
    .sort_values("Month_Number")
)

   fig14 = px.line(
    df_monthly_sales,
    x="Month",
    y="Total_Sales",
    markers=True,
    title="Total Sales by Month",
    category_orders={
        "Month": [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]
    }
)

   fig14.update_traces(
    hovertemplate="Month: %{x}<br>Sales: $%{y:,.2f}<extra></extra>"
)

   st.plotly_chart(fig14, use_container_width=True)

# Monthly Sales Trend by Region
   df_monthly_region = (
    df_filtered
    .groupby(["Month_Number", "Month", "Region"], as_index=False)["Sales"]
    .sum()
    .rename(columns={"Sales": "Total_Sales"})
    .sort_values("Month_Number")
)

   fig15 = px.line(
    df_monthly_region,
    x="Month",
    y="Total_Sales",
    color="Region",
    markers=True,
    title="Total Sales by Calendar Month and Region"
)

   fig15.update_traces(
    hovertemplate=(
        "Month: %{x}"
        "<br>Sales: $%{y:,.2f}"
        "<extra></extra>"
    )
)

   fig15.update_layout(
    xaxis_title="Month",
    yaxis_title="Total Sales",
    legend_title="Region"
)

   st.plotly_chart(fig15, use_container_width=True)

   st.subheader("Trend Analysis Conclusion")

   st.markdown("""
<p style="font-size:18px;">
<strong>Overall Trend Summary:</strong>
The business shows growth over the years, indicating an overall positive sales trajectory. 
Sales also vary across calendar months, with some months generating higher demand than others, 
which suggests seasonal purchasing patterns. The regional monthly trends provide additional 
context on whether this pattern is shared across regions and whether the South remains 
consistently behind other regions throughout the year.
</p>
""", unsafe_allow_html=True)








