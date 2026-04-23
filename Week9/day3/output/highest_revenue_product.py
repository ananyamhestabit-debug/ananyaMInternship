import pandas as pd

def find_highest_revenue_product():
    # Load the dataset
    sales_data = pd.read_csv('/home/ananyamishra/re_assignment/Week9/Day3/tools/workspace/sales.csv')

    # Assuming the dataset has columns 'product' and 'revenue'
    # Group by product and calculate total revenue
    product_revenue = sales_data.groupby('product')['revenue'].sum().reset_index()

    # Find the product with the highest total revenue
    highest_revenue_product = product_revenue.loc[product_revenue['revenue'].idxmax()]

    # Print the final answer
    print("The product with the highest total revenue is:", highest_revenue_product['product'])

# Call the function
find_highest_revenue_product()