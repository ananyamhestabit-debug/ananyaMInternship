import pandas as pd

# Load the dataset
df = pd.read_csv("/home/ananyamishra/re_assignment/Week9/Day3/tools/workspace/sales.csv")

# Convert column names to lowercase
df.columns = df.columns.str.lower().str.strip()

# Top 5 insights
print("Top 5 Insights:")
print("1. Total Sales: ", df['revenue'].sum())
print("2. Average Sales: ", df['revenue'].mean())
print("3. Top Selling Product: ", df.groupby("product")["revenue"].sum().idxmax())
print("4. Region with Highest Sales: ", df.groupby("region")["revenue"].sum().idxmax())
print("5. Sales by Channel: ", df.groupby("channel")["revenue"].sum())

# No further computation needed