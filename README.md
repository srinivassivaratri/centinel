# Centinel

A high-precision financial calculation library implementing 4-byte integer representation for monetary operations.

[![Tests](https://img.shields.io/github/workflow/status/username/centinel/tests/main)](https://github.com/username/centinel/actions)
[![PyPI version](https://img.shields.io/pypi/v/centinel.svg)](https://pypi.org/project/centinel/)
[![Python Version](https://img.shields.io/pypi/pyversions/centinel.svg)](https://pypi.org/project/centinel/)

## Features

- 🎯 4-byte integer-based calculations for maximum precision
- 💱 Thread-safe currency conversion with cross-rate support
- 📊 Advanced financial operations (compound interest, ratios)
- ⚡ High-performance optimizations for trading environments
- 🔄 Batch operations with concurrent processing
- 📝 Comprehensive test coverage
- ⚙️ Full configuration options

## Installation

```bash
pip install centinel
```

## Quick Start

```python
from centinel import Money, Currency

# Create money objects
amount1 = Money(100, Currency.USD)
amount2 = Money(50, Currency.USD)

# Basic operations
total = amount1 + amount2  # 150.00 USD
difference = amount1 - amount2  # 50.00 USD
doubled = amount1 * 2  # 200.00 USD
halved = amount1 / 2  # 50.00 USD

# Currency conversion
from centinel import convert
euros = convert(amount1, Currency.EUR)  # 85.00 EUR
```

## Advanced Features

### Currency Conversion

```python
from centinel import Money, Currency, convert, update_exchange_rate

# Update exchange rates
update_exchange_rate(Currency.USD, Currency.EUR, 0.85)

# Convert with custom rates
amount = Money(100, Currency.USD)
euros = convert(amount, Currency.EUR)  # Using updated rate

# Historical rates support
from datetime import date
store_historical_rate(Currency.USD, Currency.EUR, 0.95, date(2024, 1, 1))
historical_euros = convert(amount, Currency.EUR, date(2024, 1, 1))
```

### Financial Operations

```python
from centinel import AdvancedOperations, RoundingPolicy

# Compound interest
principal = Money(1000, Currency.USD)
result = AdvancedOperations.compound_interest(principal, 0.05, 1)  # 5% for 1 year

# Percentage calculations
amount = Money(200, Currency.USD)
percentage = AdvancedOperations.percentage_of(amount, 15)  # 15% of amount

# Rounding policies
rounded = AdvancedOperations.apply_rounding(amount, RoundingPolicy.HALF_UP)

# Financial ratios
profit_margin = AdvancedOperations.profit_margin(revenue, costs)
debt_equity = AdvancedOperations.debt_to_equity(debt, equity)
```

### Performance Optimizations

```python
from centinel import OptimizedMoney, BatchProcessor

# Optimized money operations
opt_money = OptimizedMoney(100, Currency.USD)

# Batch processing
processor = BatchProcessor()
amounts = [Money(100, Currency.USD) for _ in range(1000)]
total = processor.batch_add(amounts)
converted = processor.batch_convert(amounts, Currency.EUR)

# Performance metrics
metrics = processor.get_performance_metrics()
```

## Thread Safety

All currency conversion and exchange rate operations are thread-safe, making Centinel suitable for high-frequency trading environments. The library implements:

- Thread-safe exchange rate management
- Concurrent batch processing
- Object pooling for memory efficiency
- Optimized caching for exchange rates

## Error Handling

```python
from centinel.exceptions import MoneyOverflowError, CurrencyMismatchError

try:
    large_amount = Money(2_147_483_648, Currency.USD)  # Will raise MoneyOverflowError
except MoneyOverflowError:
    print("Amount exceeds 4-byte integer limit")

try:
    usd = Money(100, Currency.USD)
    eur = Money(100, Currency.EUR)
    total = usd + eur  # Will raise CurrencyMismatchError
except CurrencyMismatchError:
    print("Cannot add different currencies directly")
```

## Configuration Options

- Configurable rounding policies (HALF_UP, DOWN, UP)
- Custom exchange rate providers
- Batch operation settings
- Performance optimization toggles

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by Martin Fowler's [Money Pattern](https://martinfowler.com/eaaCatalog/money.html)
- Built with modern Python best practices
- Optimized for high-frequency trading environments

## Performance Benchmarks

Based on our performance tests with 100,000 operations:

- Regular Addition: ~0.092s
- Optimized Addition: ~0.036s
- Concurrent Batch Addition: ~0.039s

This represents a 2.5x performance improvement using optimized operations.
