def generate_sql(query):

    q = query.lower()

    # SHOW ALL
    if "all products" in q:
        return "SELECT * FROM products LIMIT 10"

    # PRICE
    elif "price" in q:
        return "SELECT Name, Price FROM products LIMIT 10"

    # EXPENSIVE PRODUCTS
    elif "greater than" in q or "above" in q:
        import re
        nums = re.findall(r'\d+', q)

        if nums:
            value = nums[0]
            return f"SELECT Name, Price FROM products WHERE Price > {value}"

    #  IN STOCK
    elif "in stock" in q:
        return "SELECT Name, Stock FROM products WHERE Stock > 0"

    #  OUT OF STOCK
    elif "out of stock" in q:
        return "SELECT Name, Stock FROM products WHERE Stock = 0"

    # CHEAP PRODUCTS
    elif "less than" in q or "under" in q:
        import re
        nums = re.findall(r'\d+', q)

        if nums:
            value = nums[0]
            return f"SELECT Name, Price FROM products WHERE Price < {value}"

    #  TOP PRODUCTS
    elif "top" in q:
        return "SELECT Name, Price FROM products ORDER BY Price DESC LIMIT 5"

    #  DEFAULT (NO FALLBACK DATA)
    return "SELECT * FROM products LIMIT 0"