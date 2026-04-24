import pandas as pd

# Load the dataset
df = pd.read_csv("/home/ananyamishra/re_assignment/Week9/day3/tools/workspace/sales.csv")

# Convert column names to lowercase
df.columns = df.columns.str.lower().str.strip()

# Calculate total units for each product
total_units_per_product = df.groupby("product")["units"].sum()

# Print the final answer
print(total_units_per_product)