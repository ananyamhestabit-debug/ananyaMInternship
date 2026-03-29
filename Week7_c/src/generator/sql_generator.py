def generate_sql(query):

    query = query.lower()

    if "all products" in query:
        return "SELECT * FROM products LIMIT 10"

    if "price" in query:
        return "SELECT Name, Price FROM products ORDER BY Price DESC LIMIT 5"

    if "category" in query:
        return "SELECT Category, COUNT(*) FROM products GROUP BY Category"

    if "brand" in query:
        return "SELECT Brand, COUNT(*) FROM products GROUP BY Brand"

    return "SELECT * FROM products LIMIT 5"