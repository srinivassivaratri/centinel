import pytest
from centinel import Money, Currency
from centinel.optimizations import OptimizedMoney, BatchProcessor, cached_exchange_rate
from centinel.exceptions import MoneyOverflowError

def test_optimized_money_creation():
    opt_money = OptimizedMoney(100, Currency.USD)
    assert opt_money.amount == 100
    assert opt_money.currency == Currency.USD

def test_optimized_money_conversion():
    money = Money(100, Currency.USD)
    opt_money = OptimizedMoney.from_money(money)
    assert opt_money.amount == money.amount
    assert opt_money.currency == money.currency
    
    converted_back = opt_money.to_money()
    assert converted_back.amount == money.amount
    assert converted_back.currency == money.currency

def test_optimized_money_addition():
    m1 = OptimizedMoney(100, Currency.USD)
    m2 = OptimizedMoney(50, Currency.USD)
    result = m1 + m2
    assert result.amount == 150
    assert result.currency == Currency.USD

def test_optimized_money_overflow():
    with pytest.raises(MoneyOverflowError):
        OptimizedMoney(2_147_483_648, Currency.USD)

def test_batch_processor():
    processor = BatchProcessor()
    amounts = [Money(100, Currency.USD), Money(200, Currency.USD), Money(300, Currency.USD)]
    
    # Test batch addition
    result = processor.batch_add(amounts)
    assert result.amount == 600
    assert result.currency == Currency.USD
    
    # Test batch conversion
    converted = processor.batch_convert(amounts, Currency.EUR)
    assert len(converted) == 3
    assert all(m.currency == Currency.EUR for m in converted)
    assert converted[0].amount == pytest.approx(85.0)

def test_cached_exchange_rate():
    # Test cache hit
    rate1 = cached_exchange_rate(Currency.USD, Currency.EUR)
    rate2 = cached_exchange_rate(Currency.USD, Currency.EUR)
    assert rate1 == rate2
    
    # Test same currency
    assert cached_exchange_rate(Currency.USD, Currency.USD) == 1.0

def test_performance_metrics():
    processor = BatchProcessor()
    amounts = [Money(100, Currency.USD), Money(200, Currency.USD)]
    
    # Perform some operations
    processor.batch_add(amounts)
    processor.batch_convert(amounts, Currency.EUR)
    
    # Check metrics
    metrics = processor.get_performance_metrics()
    assert "batch_add" in metrics
    assert "batch_convert" in metrics
    
    for op in ["batch_add", "batch_convert"]:
        assert "avg_time" in metrics[op]
        assert "min_time" in metrics[op]
        assert "max_time" in metrics[op]
        assert "count" in metrics[op]
        assert metrics[op]["count"] == 1
