from enum import Enum
from typing import Union, Optional
from .exceptions import MoneyOverflowError, InvalidAmountError
from .currency import Currency

class Operation(Enum):
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"

class Money:
    """
    Represents a monetary value using a 4-byte integer.
    Stores amounts in smallest currency units (e.g., cents).
    """
    MAX_VALUE = 2_147_483_647  # Maximum value for 4-byte signed integer
    MIN_VALUE = -2_147_483_648

    def __init__(self, amount: Union[int, float], currency: Currency):
        """
        Initialize Money object with amount and currency.
        
        Args:
            amount: Amount in currency units (e.g., dollars)
            currency: Currency enum value
        """
        # Convert to smallest currency unit
        if isinstance(amount, float):
            amount = round(amount * 100)
        elif isinstance(amount, int):
            amount *= 100
        else:
            raise InvalidAmountError("Amount must be numeric")

        if not self.MIN_VALUE <= amount <= self.MAX_VALUE:
            raise MoneyOverflowError("Amount exceeds 4-byte integer limits")

        self._amount = amount
        self._currency = currency

    @property
    def amount(self) -> float:
        """Get amount in currency units."""
        return self._amount / 100

    @property
    def currency(self) -> Currency:
        """Get currency."""
        return self._currency

    def _validate_operation(self, other: 'Money', op: Operation) -> None:
        """Validate operation between two Money objects."""
        if not isinstance(other, Money):
            raise TypeError("Operations only supported between Money objects")
        if self.currency != other.currency:
            raise ValueError("Cannot operate on different currencies")

    def __add__(self, other: 'Money') -> 'Money':
        self._validate_operation(other, Operation.ADD)
        result = self._amount + other._amount
        if not self.MIN_VALUE <= result <= self.MAX_VALUE:
            raise MoneyOverflowError("Addition would exceed integer limits")
        return Money(result/100, self.currency)

    def __sub__(self, other: 'Money') -> 'Money':
        self._validate_operation(other, Operation.SUBTRACT)
        result = self._amount - other._amount
        if not self.MIN_VALUE <= result <= self.MAX_VALUE:
            raise MoneyOverflowError("Subtraction would exceed integer limits")
        return Money(result/100, self.currency)

    def __mul__(self, factor: Union[int, float]) -> 'Money':
        if not isinstance(factor, (int, float)):
            raise TypeError("Can only multiply by numeric values")
        result = round(self._amount * factor)
        if not self.MIN_VALUE <= result <= self.MAX_VALUE:
            raise MoneyOverflowError("Multiplication would exceed integer limits")
        return Money(result/100, self.currency)

    def __truediv__(self, factor: Union[int, float]) -> 'Money':
        if not isinstance(factor, (int, float)):
            raise TypeError("Can only divide by numeric values")
        if factor == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        result = round(self._amount / factor)
        return Money(result/100, self.currency)

    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency.value}"

    def __repr__(self) -> str:
        return f"Money({self.amount}, {self.currency})"