from typing import Dict, List, Tuple, Optional, Union
from functools import lru_cache
import time
import statistics
from threading import Lock
from array import array
from .core import Money, Operation
from .currency import Currency, exchange_manager
from .exceptions import MoneyOverflowError

class MoneyPool:
    """Object pool for OptimizedMoney instances to reduce allocation overhead."""
    def __init__(self, initial_size: int = 1000):
        self._lock = Lock()
        self._pool = []
        self._expand(initial_size)

    def _expand(self, size: int):
        for _ in range(size):
            obj = OptimizedMoney.__new__(OptimizedMoney)
            self._pool.append(obj)

    def acquire(self) -> 'OptimizedMoney':
        with self._lock:
            if not self._pool:
                self._expand(1000)
            return self._pool.pop()

    def release(self, obj: 'OptimizedMoney'):
        with self._lock:
            self._pool.append(obj)

class PerformanceMetrics:
    """Track and store performance metrics for operations."""
    def __init__(self):
        self._lock = Lock()
        self.operation_times: Dict[str, List[float]] = {}
        self.operation_counts: Dict[str, int] = {}
    
    def record_operation(self, operation: str, duration: float):
        """Record the duration of an operation."""
        with self._lock:
            if operation not in self.operation_times:
                self.operation_times[operation] = []
                self.operation_counts[operation] = 0
            self.operation_times[operation].append(duration)
            self.operation_counts[operation] += 1
    
    def get_metrics(self, operation: str) -> Dict[str, float]:
        """Get performance metrics for a specific operation."""
        with self._lock:
            if operation not in self.operation_times:
                return {}
            times = self.operation_times[operation]
            return {
                'avg_time': statistics.mean(times),
                'min_time': min(times),
                'max_time': max(times),
                'count': self.operation_counts[operation]
            }

class OptimizedMoney:
    """Optimized version of Money class for high-frequency operations."""
    __slots__ = ('_amount', '_currency', '_lock')
    
    def __init__(self, amount: Union[int, float], currency: Currency):
        # Store amount directly in cents/smallest unit for faster operations
        self._amount = int(round(amount * 100)) if isinstance(amount, float) else amount * 100
        if not Money.MIN_VALUE <= self._amount <= Money.MAX_VALUE:
            raise MoneyOverflowError("Amount exceeds 4-byte integer limits")
        self._currency = currency
        self._lock = Lock()

    @property
    def amount(self) -> float:
        return self._amount / 100

    @property
    def currency(self) -> Currency:
        return self._currency

    @staticmethod
    def from_money(money: Money) -> 'OptimizedMoney':
        """Convert regular Money object to OptimizedMoney."""
        obj = _money_pool.acquire()
        obj._amount = int(round(money.amount * 100))
        obj._currency = money.currency
        return obj

    def to_money(self) -> Money:
        """Convert back to regular Money object."""
        result = Money(self.amount, self.currency)
        _money_pool.release(self)
        return result

    def __add__(self, other: 'OptimizedMoney') -> 'OptimizedMoney':
        with self._lock:
            if self.currency != other.currency:
                raise ValueError("Cannot operate on different currencies")
            result = self._amount + other._amount
            if not Money.MIN_VALUE <= result <= Money.MAX_VALUE:
                raise MoneyOverflowError("Addition would exceed integer limits")
            new_obj = _money_pool.acquire()
            new_obj._amount = result
            new_obj._currency = self.currency
            return new_obj

# Global money pool
_money_pool = MoneyPool()

@lru_cache(maxsize=2048)
def cached_exchange_rate(from_currency: Currency, to_currency: Currency) -> float:
    """Cached version of exchange rate lookup with increased cache size."""
    if from_currency == to_currency:
        return 1.0
    return exchange_manager.get_rate(from_currency, to_currency)

class BatchProcessor:
    """Process multiple money operations in batch for improved performance."""
    def __init__(self):
        self.performance_metrics = PerformanceMetrics()
        self._lock = Lock()

    def _vectorized_add(self, amounts: array) -> int:
        """Vectorized addition of amounts stored in array."""
        return sum(amounts)

    def batch_add(self, amounts: List[Money]) -> Money:
        """Add multiple Money objects efficiently using vectorized operations."""
        start_time = time.perf_counter()
        
        if not amounts:
            raise ValueError("Cannot process empty batch")
        
        with self._lock:
            # Convert to array for vectorized operations
            amounts_array = array('l', [int(round(m.amount * 100)) for m in amounts])
            currency = amounts[0].currency
            
            # Verify currency consistency
            if not all(m.currency == currency for m in amounts):
                raise ValueError("All amounts must have same currency")
            
            # Perform vectorized addition
            result = self._vectorized_add(amounts_array)
            
            if not Money.MIN_VALUE <= result <= Money.MAX_VALUE:
                raise MoneyOverflowError("Batch addition would exceed integer limits")
            
            end_time = time.perf_counter()
            self.performance_metrics.record_operation("batch_add", end_time - start_time)
            
            return Money(result/100, currency)

    def batch_convert(self, amounts: List[Money], target_currency: Currency) -> List[Money]:
        """Convert multiple Money objects to target currency efficiently."""
        start_time = time.perf_counter()
        
        if not amounts:
            raise ValueError("Cannot process empty batch")
        
        with self._lock:
            # Pre-calculate exchange rates
            source_currencies = {m.currency for m in amounts}
            rates = {curr: cached_exchange_rate(curr, target_currency) for curr in source_currencies}
            
            # Vectorized conversion
            results = []
            batch_size = 1000
            for i in range(0, len(amounts), batch_size):
                batch = amounts[i:i + batch_size]
                converted_amounts = array('d', [m.amount * rates[m.currency] for m in batch])
                results.extend([Money(amt, target_currency) for amt in converted_amounts])
            
            end_time = time.perf_counter()
            self.performance_metrics.record_operation("batch_convert", end_time - start_time)
            
            return results

    def get_performance_metrics(self) -> Dict[str, Dict[str, float]]:
        """Get performance metrics for all operations."""
        return {
            op: self.performance_metrics.get_metrics(op)
            for op in ["batch_add", "batch_convert"]
        }
