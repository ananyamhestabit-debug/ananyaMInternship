import pandas as pd

# Load dataset
df = pd.read_csv("/home/ananyamishra/re_assignment/Week9/Day3/tools/workspace/sales.csv")

# Convert column names to lowercase
df.columns = df.columns.str.lower().str.strip()

# Filter and aggregate data
total_units = df.groupby("region")["units"].sum()

# Print final answer
print("Total units by region:")
print(total_units)