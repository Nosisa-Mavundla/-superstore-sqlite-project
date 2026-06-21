import pandas as pd
df = pd.read_csv("data/superstore.csv")

#Convert data type
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)
df["Sales"] =pd.to_numeric(df["Sales"])
df["Postal Code"]=df["Postal Code"].astype(str).str.replace(".0", "" , regex=False)

#Clean data for data quality and governace
print(df.dtypes)
print(df.head(10))
print("Duplicated rows: ", df.duplicated().sum())
print("Missing Values: ", df.isnull().sum())
print(df.dtypes)
print(df.columns)
print(df.describe())
print(df["Region"].unique())
print(df["Category"].unique())