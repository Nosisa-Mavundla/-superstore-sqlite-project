import sqlite3
import pandas as pd
df=pd.read_csv("data/superstore.csv")

conn = sqlite3.connect("database/superstore.db")
cursor = conn.cursor()

print("Connected to SQLITE database successfully.")

#SQL Analysis
#The Total Sales made by superstore across all regions.
query = """
SELECT SUM(Sales) AS Total_Sales
FROM superstore
"""
cursor= cursor.execute(query)
result = cursor.fetchone()
print("The Total Sales are: ", result[0])


#Sales performance by Region
query ="""
SELECT Region, SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY Region
ORDER BY Total_Sales DESC
"""
cursor= cursor.execute(query)
result= cursor.fetchall()

print("The total sales by Regions are:")
for Region, Sales in result:
 print( Region, Sales)

#Total Sales by Category
query ="""
SELECT Category, SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY Category
ORDER BY Total_Sales DESC
"""
cursor.execute(query)
result = cursor.fetchall()

for Category, Sales in result:
 print(Category, Sales)

 #Sales by sub-category
 query = """
SELECT "Sub-Category", SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY "Sub-Category"
ORDER BY Total_Sales DESC
"""
cursor.execute(query)
result= cursor.fetchall()

for Sub_Category, Sales in result:
 print(Sub_Category, Sales)

#Sales by consumer segment
print(df.columns)
query = """
SELECT Segment, SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY Segment
ORDER BY Total_Sales DESC
"""
cursor.execute(query)
result = cursor.fetchall()

for Segment, Sales in result:
 print(Segment, Sales)

#Top 10 performing Products
#Sales by products
query = """
SELECT "Product Name", SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY "Product Name"
ORDER BY Total_Sales DESC 
LIMIT 10
"""
cursor.execute(query)
result = cursor.fetchall()
for Product_Name, Sales in result:
 print(Product_Name, Sales)

#Sales by State
query= """
SELECT State, SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY State
ORDER BY Total_Sales DESC

"""
cursor.execute(query)
result= cursor.fetchall()

for State, Sales in result:
 print(State, Sales)

#TOP 10 Cities generating the most sales
#Sales by City
query= """
SELECT City, SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY City
ORDER BY Sales DESC
LIMIT 10
"""
cursor.execute(query)
result= cursor.fetchall()
for City, Sales in result:
 print(City, Sales)

 #Sales by Year
query="""
SELECT strftime("%Y", "Order Date") AS Year, SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY Year
ORDER BY Total_Sales DESC
"""
cursor.execute(query)
result= cursor.fetchall()
for Year, Total_Sales in result:
 print(Year, Total_Sales)

#Sales by month
query="""
SELECT strftime("%m", "Order Date") AS Month, SUM(Sales)AS Total_Sales
FROM superstore
GROUP BY Month
ORDER BY Total_Sales DESC
"""
cursor.execute(query)
result= cursor.fetchall()
for Month,Total_Sales in result:
 print(Month, Total_Sales)

 #Sales by each month in each year
 query ="""
SELECT strftime("%Y-%m", "Order Date") AS Year_Month, SUM(Sales)AS Total_Sales
FROM superstore
GROUP BY Year_Month
ORDER BY Year_Month;
"""
cursor.execute(query)
result= cursor.fetchall()
for Year_Month, Sales in result:
 print(Year_Month, Sales)

 query="""
SELECT "Order Date"
FROM superstore
LIMIT 10
"""
cursor.execute(query)
result= cursor.fetchall()
for date in result:
 print(date)