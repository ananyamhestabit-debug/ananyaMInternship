def validate_sql(query):
    q = query.lower()

    if not q.strip().startswith("select"):
        return False, "Only SELECT allowed"

    for word in ["drop", "delete", "update", "insert"]:
        if word in q:
            return False, "Unsafe query"

    return True, "Valid"