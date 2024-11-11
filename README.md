# Centinel

A high-precision financial calculation library implementing 4-byte integer representation for monetary operations.

[![Tests](https://img.shields.io/github/workflow/status/username/centinel/tests/main)](https://github.com/username/centinel/actions)
[![PyPI version](https://img.shields.io/pypi/v/centinel.svg)](https://pypi.org/project/centinel/)
[![Python Version](https://img.shields.io/pypi/pyversions/centinel.svg)](https://pypi.org/project/centinel/)

## Why?

Financial calculations require absolute precision and reliability. Traditional floating-point arithmetic can lead to rounding errors and precision loss, which is unacceptable in financial systems where even tiny discrepancies can result in significant monetary impacts. Centinel addresses these challenges through several key design decisions:

### 1. Integer-Based Precision

Instead of using floating-point numbers, Centinel uses 4-byte integers to represent monetary values (storing amounts in smallest currency units, e.g., cents). This approach:
- Eliminates floating-point rounding errors
- Guarantees exact arithmetic operations
- Prevents precision loss in calculations
- Ensures consistent results across different platforms

### 2. Thread-Safe Design

Modern financial systems, especially in trading environments, require concurrent processing of numerous transactions. Centinel is built with thread-safety at its core:
- Thread-safe exchange rate management prevents race conditions
- Concurrent batch processing enables efficient handling of multiple operations
- Object pooling reduces memory allocation overhead
- Optimized caching improves performance in high-frequency scenarios

### 3. Performance Focus

High-frequency trading environments demand both speed and accuracy. Centinel achieves this through:
- Efficient 4-byte integer operations
- Vectorized batch processing capabilities
- Minimal memory footprint
- Optimized algorithms for common financial calculations

### 4. Comprehensive Financial Support

Beyond basic arithmetic, financial systems need robust support for:
- Currency conversion with cross-rates
- Historical exchange rates
- Compound interest calculations
- Financial ratio computations
- Configurable rounding policies

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

Please ensure your PR:
- Includes tests for new functionality
- Updates documentation as needed
- Follows the existing code style
- Includes a clear description of changes

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
