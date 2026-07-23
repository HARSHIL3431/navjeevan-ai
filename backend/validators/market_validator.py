def validate_market_quantity(quantity: float) -> float:
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")
    return quantity
