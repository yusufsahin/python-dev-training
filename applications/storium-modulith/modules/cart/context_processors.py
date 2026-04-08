def cart_context(request):
    session = getattr(request, "session", {})
    cart_data = session.get("cart", {})
    item_count = sum(item["quantity"] for item in cart_data.values())
    return {"cart_item_count": item_count}
