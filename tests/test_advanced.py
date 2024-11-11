import pytest
from decimal import Decimal
from centinel import Money, Currency, AdvancedOperations, RoundingPolicy

def test_compound_interest():
    principal = Money(1000, Currency.USD)
    result = AdvancedOperations.compound_interest(principal, 0.05, 1)
    assert result.amount == pytest.approx(1051.16, rel=1e-4)

def test_percentage_calculation():
    amount = Money(200, Currency.USD)
    result = AdvancedOperations.percentage_of(amount, 15)
    assert result.amount == 30.0

def test_rounding_policies():
    amount = Money(100.126, Currency.USD)
    
    # Test HALF_UP
    rounded = AdvancedOperations.apply_rounding(amount, RoundingPolicy.HALF_UP)
    assert rounded.amount == 100.13
    
    # Test DOWN
    rounded = AdvancedOperations.apply_rounding(amount, RoundingPolicy.DOWN)
    assert rounded.amount == 100.12
    
    # Test UP
    rounded = AdvancedOperations.apply_rounding(amount, RoundingPolicy.UP)
    assert rounded.amount == 100.13

def test_financial_ratios():
    # Test profit margin
    revenue = Money(1000, Currency.USD)
    costs = Money(600, Currency.USD)
    margin = AdvancedOperations.profit_margin(revenue, costs)
    assert margin == pytest.approx(0.4)
    
    # Test debt to equity
    debt = Money(500, Currency.USD)
    equity = Money(1000, Currency.USD)
    ratio = AdvancedOperations.debt_to_equity(debt, equity)
    assert ratio == 0.5

def test_batch_operations():
    amounts = [
        Money(100, Currency.USD),
        Money(200, Currency.USD),
        Money(300, Currency.USD)
    ]
    
    # Test sum
    result = AdvancedOperations.batch_operation(amounts, "sum")
    assert result.amount == 600
    
    # Test average
    result = AdvancedOperations.batch_operation(amounts, "average")
    assert result.amount == 200
    
    # Test max
    result = AdvancedOperations.batch_operation(amounts, "max")
    assert result.amount == 300
    
    # Test min
    result = AdvancedOperations.batch_operation(amounts, "min")
    assert result.amount == 100

def test_invalid_parameters():
    with pytest.raises(ValueError):
        AdvancedOperations.compound_interest(Money(100, Currency.USD), -0.05, 1)
    
    with pytest.raises(ValueError):
        AdvancedOperations.percentage_of(Money(100, Currency.USD), 101)
    
    with pytest.raises(ValueError):
        amounts = [Money(100, Currency.USD), Money(100, Currency.EUR)]
        AdvancedOperations.batch_operation(amounts, "sum")
