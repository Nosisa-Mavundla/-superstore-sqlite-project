import sqlite3
conn = sqlite3.connect("database/superstore.db")
cursor = conn.cursor()

print("Connected to the database successfully!")

#Businessquestion: Why is the Soth region underperforming, What are the drivers of South's underperformance?
#Diagnostic Analysis
#Hypothesis1: South Region is generating fewer orders compared to other regions
#Analysis: Compare all regions' total number of unique orders
#Sql analysis(Order Volume)
query = """
SELECT Region, COUNT(DISTINCT "Order ID") AS Total_Orders
FROM superstore
GROUP BY region
ORDER BY Total_Orders ASC
"""
cursor.execute(query)
result= cursor.fetchall()
for Region, Total_Orders in result:
    print(Region, Total_Orders)

#Insight/finding
#From the sql analysis we can derive that the south region generates the lowest total number of unique orders compared to all other regions.

#By that we can conclude that South's underperformance is partially driven by the lower customer demand since it's only generating fewer
#orders compared to other regions.

#Hypothesis2: South Region has the lowest Average Order Value compared to other regions/Customers in South are spending less per order
#Analysis: Compare Average Order Value across all regions
#Sql analysis(AOV)
query ="""
SELECT Region,(SUM(Sales)/COUNT(DISTINCT "Order ID")) AS AOV
FROM superstore
GROUP BY Region
ORDER BY AOV ASC
"""
cursor.execute(query)
result= cursor.fetchall()
for Region, AOV in result:
    print(Region, AOV)

#Insight: Customere is South Are spending more per order compared to order regions
#Thus: AOV Is not even partially a driver of South's Underperfromance

#Hypothesis3:Category Performance is driving the sales gap 
#Analysis: Compare sales of each product category among all regions
#sql analysis(Product mix)
query ="""
SELECT Region, Category, SUM(Sales) AS Total_Sales
FROM superstore
GROUP BY Region, Category
ORDER BY Region, Total_Sales ASC
"""
cursor.execute(query)
result = cursor.fetchall()
for Region, Category, Sales in result:
    print(Region, Category, Sales)
#Insight: South generated the lowest sales across all product categories compared to other regions
#by that we can conclude that south's underperfromance is partially driven by the product category's gap