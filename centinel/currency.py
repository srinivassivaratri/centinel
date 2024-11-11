from enum import Enum
from typing import Dict, Tuple, Optional
from datetime import datetime, date
from threading import Lock
from .exceptions import CurrencyMismatchError

class Currency(Enum):
    """Supported currencies."""
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"

class ExchangeRateManager:
    """Manages exchange rates with thread-safe operations and cross-rate calculations."""
    def __init__(self):
        self._lock = Lock()
        self._rates: Dict[Tuple[Currency, Currency], float] = {
            (Currency.USD, Currency.EUR): 0.85,
            (Currency.USD, Currency.GBP): 0.73,
            (Currency.USD, Currency.JPY): 110.0,
            (Currency.EUR, Currency.USD): 1.18,
            (Currency.EUR, Currency.GBP): 0.86,
            (Currency.EUR, Currency.JPY): 129.5,
            (Currency.GBP, Currency.USD): 1.37,
            (Currency.GBP, Currency.EUR): 1.16,
            (Currency.GBP, Currency.JPY): 150.7,
            (Currency.JPY, Currency.USD): 0.0091,
            (Currency.JPY, Currency.EUR): 0.0077,
            (Currency.JPY, Currency.GBP): 0.0066,
        }
        self._historical_rates: Dict[date, Dict[Tuple[Currency, Currency], float]] = {}

    def get_rate(self, from_currency: Currency, to_currency: Currency) -> float:
        """Get current exchange rate with cross-rate calculation if direct rate unavailable."""
        if from_currency == to_currency:
            return 1.0

        with self._lock:
            rate_key = (from_currency, to_currency)
            if rate_key in self._rates:
                return self._rates[rate_key]
            
            # Try USD as intermediate currency for cross-rate
            try:
                usd_rate1 = self.get_rate(from_currency, Currency.USD)
                usd_rate2 = self.get_rate(Currency.USD, to_currency)
                return usd_rate1 * usd_rate2
            except CurrencyMismatchError:
                # Try EUR as intermediate currency
                try:
                    eur_rate1 = self.get_rate(from_currency, Currency.EUR)
                    eur_rate2 = self.get_rate(Currency.EUR, to_currency)
                    return eur_rate1 * eur_rate2
                except CurrencyMismatchError:
                    raise CurrencyMismatchError(f"No exchange rate path from {from_currency} to {to_currency}")

    def update_rate(self, from_currency: Currency, to_currency: Currency, rate: float) -> None:
        """Update exchange rate with validation."""
        if rate <= 0:
            raise ValueError("Exchange rate must be positive")
        
        with self._lock:
            self._rates[(from_currency, to_currency)] = rate
            # Update inverse rate
            self._rates[(to_currency, from_currency)] = 1.0 / rate

    def get_historical_rate(self, from_currency: Currency, to_currency: Currency, 
                          rate_date: date) -> float:
        """Get historical exchange rate for a specific date."""
        with self._lock:
            if rate_date not in self._historical_rates:
                raise ValueError(f"No historical rates available for {rate_date}")
            
            rates = self._historical_rates[rate_date]
            rate_key = (from_currency, to_currency)
            
            if rate_key not in rates:
                raise CurrencyMismatchError(
                    f"No historical rate available for {from_currency} to {to_currency} on {rate_date}")
            
            return rates[rate_key]

    def store_historical_rate(self, from_currency: Currency, to_currency: Currency,
                            rate: float, rate_date: date) -> None:
        """Store historical exchange rate."""
        if rate <= 0:
            raise ValueError("Exchange rate must be positive")
        
        with self._lock:
            if rate_date not in self._historical_rates:
                self._historical_rates[rate_date] = {}
            
            self._historical_rates[rate_date][(from_currency, to_currency)] = rate
            self._historical_rates[rate_date][(to_currency, from_currency)] = 1.0 / rate

# Global exchange rate manager instance
exchange_manager = ExchangeRateManager()

def convert(amount: 'Money', target_currency: Currency, rate_date: Optional[date] = None) -> 'Money':
    """
    Convert money from one currency to another.
    
    Args:
        amount: Money object to convert
        target_currency: Currency to convert to
        rate_date: Optional date for historical conversion
    
    Returns:
        New Money object in target currency
    """
    from .core import Money

    if amount.currency == target_currency:
        return amount

    try:
        if rate_date:
            rate = exchange_manager.get_historical_rate(amount.currency, target_currency, rate_date)
        else:
            rate = exchange_manager.get_rate(amount.currency, target_currency)
    except (CurrencyMismatchError, ValueError) as e:
        raise CurrencyMismatchError(f"Currency conversion failed: {str(e)}")

    converted_amount = amount.amount * rate
    return Money(converted_amount, target_currency)

def update_exchange_rate(from_currency: Currency, to_currency: Currency, rate: float) -> None:
    """Update the exchange rate between two currencies."""
    exchange_manager.update_rate(from_currency, to_currency, rate)

def store_historical_rate(from_currency: Currency, to_currency: Currency,
                         rate: float, rate_date: date) -> None:
    """Store a historical exchange rate."""
    exchange_manager.store_historical_rate(from_currency, to_currency, rate, rate_date)
