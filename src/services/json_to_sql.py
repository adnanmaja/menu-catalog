def json_to_sql(Menu, filters):
    query = Menu.query
    
    if "name_contains" in filters and filters["name_contains"]:
        name_filter = filters["name_contains"]
  
        if isinstance(name_filter, list): # list
            for term in name_filter:
                query = query.filter(Menu.name.ilike(f"%{term}%"))
        else:
            # string
            query = query.filter(Menu.name.ilike(f"%{name_filter}%"))

    if filters.get("category"):
        query = query.filter(Menu.category == filters["category"])

    if filters.get("min_price") is not None:
        query = query.filter(Menu.price >= filters["min_price"])

    if filters.get("max_price") is not None:
        query = query.filter(Menu.price <= filters["max_price"])

    if filters.get("min_calories") is not None:
        query = query.filter(Menu.calories >= filters["min_calories"])

    if filters.get("max_calories") is not None:
        query = query.filter(Menu.calories <= filters["max_calories"])

    return query
