import pandas as pd

# Load the dataset
df = pd.read_csv("/home/ananyamishra/re_assignment/Week9/Day3/tools/workspace/sales.csv")

# Convert column names to lowercase
df.columns = df.columns.str.lower().str.strip()

# Check if 'revenue' column exists
if 'revenue' in df.columns:
    # Calculate the total revenue
    total_revenue = df['revenue'].sum()
    print("Total Revenue:", total_revenue)
else:
    print("Revenue column not found in the dataset.")