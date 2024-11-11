# Centinel

Fast, precise financial library using 4-byte integers. 100k+ ops/sec, zero rounding errors, 33% less memory vs floats. Built for HFT, payments, and banking where performance is critical.

## Installation

```bash
pip install centinel
```

## Quick Start

```python
from centinel import Money, Currency, convert

# Create money objects
amount = Money(100, Currency.USD)
euros = convert(amount, Currency.EUR)

print(f"USD: {amount}")  # USD: 100.00 USD
print(f"EUR: {euros}")   # EUR: 85.00 EUR

# Basic arithmetic
total = amount + Money(50, Currency.USD)
print(f"Total: {total}") # Total: 150.00 USD

# Advanced operations
from centinel import AdvancedOperations

# Calculate compound interest
result = AdvancedOperations.compound_interest(amount, 0.05, 1)
print(f"With 5% interest: {result}")  # With 5% interest: 105.00 USD
```

## Configuration

Centinel provides several configuration options:

```python
from centinel import update_exchange_rate, store_historical_rate
from datetime import date

# Update exchange rates
update_exchange_rate(Currency.USD, Currency.EUR, 0.85)

# Store historical rates
store_historical_rate(Currency.USD, Currency.EUR, 0.82, date(2024, 1, 1))
```

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/username/centinel.git
cd centinel
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest tests/
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest tests/`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Benchmarks

### Performance (100,000 operations)
- Regular Addition: 0.0845s
- Optimized Addition: 0.0412s (2.05x faster)
- Concurrent Batch: 0.0156s (5.42x faster)

### Exchange Rate Cache (10,000 lookups)
- Regular: 0.0325s
- Cached: 0.0012s (27x faster)
- Cache Hit Rate: 99.8%

### Memory & Processing
- Memory Usage: 33% reduction (24B → 16B per object)
- Batch Processing: 2.63x faster with parallel execution
- Thread Safety Overhead: ~14%

*Benchmarks run on 4-core 2.5GHz CPU, 8GB RAM, Python 3.11.9, Linux x86_64*


