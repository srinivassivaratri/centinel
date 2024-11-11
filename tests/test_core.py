import pytest
from centinel import Money, Currency
from centinel.exceptions import MoneyOverflowError, InvalidAmountError

def test_money_creation():
    m = Money(100, Currency.USD)
    assert m.amount == 100
    assert m.currency == Currency.USD

def test_money_overflow():
    with pytest.raises(MoneyOverflowError):
        Money(2_147_483_648, Currency.USD)

def test_invalid_amount():
    with pytest.raises(InvalidAmountError):
        Money("invalid", Currency.USD)

def test_addition():
    m1 = Money(100, Currency.USD)
    m2 = Money(50, Currency.USD)
    result = m1 + m2
    assert result.amount == 150
    assert result.currency == Currency.USD

def test_subtraction():
    m1 = Money(100, Currency.USD)
    m2 = Money(50, Currency.USD)
    result = m1 - m2
    assert result.amount == 50
    assert result.currency == Currency.USD

def test_multiplication():
    m = Money(100, Currency.USD)
    result = m * 2
    assert result.amount == 200
    assert result.currency == Currency.USD

def test_division():
    m = Money(100, Currency.USD)
    result = m / 2
    assert result.amount == 50
    assert result.currency == Currency.USD

def test_precision():
    m = Money(100.125, Currency.USD)
    assert m.amount == 100.13  # Rounds to nearest cent
