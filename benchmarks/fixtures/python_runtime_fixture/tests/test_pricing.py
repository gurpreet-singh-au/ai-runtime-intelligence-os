from decimal import Decimal

from runtime_fixture.pricing import calculate_order_total


def test_discount_applies_to_subtotal_not_shipping():
    assert calculate_order_total(Decimal("100.00"), Decimal("10"), Decimal("20.00")) == Decimal("110.00")


def test_zero_discount():
    assert calculate_order_total(Decimal("100.00"), Decimal("0"), Decimal("20.00")) == Decimal("120.00")


def test_full_discount_keeps_shipping():
    assert calculate_order_total(Decimal("100.00"), Decimal("100"), Decimal("20.00")) == Decimal("20.00")
