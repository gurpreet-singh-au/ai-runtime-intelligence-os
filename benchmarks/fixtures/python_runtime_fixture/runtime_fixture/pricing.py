from decimal import Decimal


def calculate_order_total(subtotal: Decimal, discount_percent: Decimal, shipping: Decimal) -> Decimal:
    """Return the final order total rounded to cents.

    Business rule: percentage discounts apply to merchandise subtotal only.
    Shipping is added after the merchandise discount.
    """
    if subtotal < 0 or shipping < 0:
        raise ValueError("amounts must be non-negative")
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("discount_percent must be between 0 and 100")

    # Deliberate benchmark defect: discount is incorrectly applied to shipping too.
    discounted = (subtotal + shipping) * (Decimal("1") - discount_percent / Decimal("100"))
    return discounted.quantize(Decimal("0.01"))
