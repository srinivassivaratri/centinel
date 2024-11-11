import pytest
from datetime import date
from centinel import Money, Currency, convert, update_exchange_rate, store_historical_rate
from centinel.exceptions import CurrencyMismatchError
from centinel.currency import exchange_manager

def test_currency_conversion():
    m = Money(100, Currency.USD)
    converted = convert(m, Currency.EUR)
    assert converted.currency == Currency.EUR
    assert converted.amount == pytest.approx(85.0)

def test_same_currency_conversion():
    m = Money(100, Currency.USD)
    converted = convert(m, Currency.USD)
    assert converted == m

def test_cross_rate_conversion():
    # Test conversion using intermediate currency
    m = Money(100, Currency.GBP)
    converted = convert(m, Currency.JPY)
    assert converted.currency == Currency.JPY
    assert converted.amount == pytest.approx(150.7 * 100)

def test_update_exchange_rate():
    # Update USD to EUR rate
    original_rate = exchange_manager.get_rate(Currency.USD, Currency.EUR)
    try:
        update_exchange_rate(Currency.USD, Currency.EUR, 0.9)
        assert exchange_manager.get_rate(Currency.USD, Currency.EUR) == 0.9
        assert exchange_manager.get_rate(Currency.EUR, Currency.USD) == pytest.approx(1/0.9)
    finally:
        # Restore original rate
        update_exchange_rate(Currency.USD, Currency.EUR, original_rate)

def test_invalid_exchange_rate():
    with pytest.raises(ValueError):
        update_exchange_rate(Currency.USD, Currency.EUR, -1.0)

def test_historical_rates():
    test_date = date(2024, 1, 1)
    historical_rate = 0.95
    
    # Store historical rate
    store_historical_rate(Currency.USD, Currency.EUR, historical_rate, test_date)
    
    # Test conversion with historical rate
    m = Money(100, Currency.USD)
    converted = convert(m, Currency.EUR, test_date)
    assert converted.currency == Currency.EUR
    assert converted.amount == pytest.approx(100 * historical_rate)

def test_invalid_historical_date():
    invalid_date = date(2020, 1, 1)
    m = Money(100, Currency.USD)
    with pytest.raises(CurrencyMismatchError):
        convert(m, Currency.EUR, invalid_date)

def test_invalid_conversion():
    # Test with unsupported currency string
    with pytest.raises(ValueError, match="'INVALID' is not a valid Currency"):
        Currency("INVALID")
    
    # Test with invalid currency type during conversion
    m = Money(100, Currency.USD)
    with pytest.raises(AttributeError):
        convert(m, "INVALID")
