import pandas as pd

# Load dataset
df = pd.read_csv("/home/ananyamishra/re_assignment/Week9/Day3/tools/workspace/sales.csv")

# Convert column names to lowercase
df.columns = df.columns.str.lower().str.strip()

# Find top product by total revenue
top_product = df.groupby("product")["revenue"].sum().idxmax()

print("Top product by total revenue:", top_product)