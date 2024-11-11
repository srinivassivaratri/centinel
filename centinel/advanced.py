from typing import List, Union, Optional
from decimal import Decimal
from .core import Money
from .currency import Currency
from .exceptions import InvalidAmountError

class AdvancedOperations:
    @staticmethod
    def compound_interest(
        principal: Money,
        rate: float,
        time: float,
        compounds_per_year: int = 12
    ) -> Money:
        """
        Calculate compound interest.
        
        Args:
            principal: Initial amount
            rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
            time: Time in years
            compounds_per_year: Number of times interest is compounded per year
        """
        if rate < 0 or time < 0 or compounds_per_year < 1:
            raise ValueError("Invalid parameters for compound interest calculation")
            
        # Using the compound interest formula: A = P(1 + r/n)^(nt)
        factor = (1 + rate/compounds_per_year) ** (compounds_per_year * time)
        return principal * factor

    @staticmethod
    def percentage_of(amount: Money, percentage: float) -> Money:
        """Calculate percentage of an amount."""
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100")
        return amount * (percentage / 100)

    @staticmethod
    def profit_margin(revenue: Money, costs: Money) -> float:
        """Calculate profit margin ratio."""
        if revenue.currency != costs.currency:
            raise ValueError("Revenue and costs must be in same currency")
        if revenue.amount == 0:
            raise ValueError("Revenue cannot be zero")
        return (revenue.amount - costs.amount) / revenue.amount

    @staticmethod
    def debt_to_equity(total_debt: Money, total_equity: Money) -> float:
        """Calculate debt to equity ratio."""
        if total_debt.currency != total_equity.currency:
            raise ValueError("Debt and equity must be in same currency")
        if total_equity.amount == 0:
            raise ValueError("Equity cannot be zero")
        return total_debt.amount / total_equity.amount

    @staticmethod
    def batch_operation(
        amounts: List[Money],
        operation: str = "sum"
    ) -> Money:
        """
        Perform batch operations on multiple money amounts.
        
        Args:
            amounts: List of Money objects
            operation: Operation to perform ("sum", "average", "max", "min")
        """
        if not amounts:
            raise ValueError("Cannot perform batch operation on empty list")
            
        # Verify all amounts have same currency
        currency = amounts[0].currency
        if not all(m.currency == currency for m in amounts):
            raise ValueError("All amounts must have same currency")

        if operation == "sum":
            result = amounts[0]
            for amount in amounts[1:]:
                result += amount
            return result
            
        elif operation == "average":
            total = AdvancedOperations.batch_operation(amounts, "sum")
            return Money(total.amount / len(amounts), total.currency)
            
        elif operation == "max":
            return max(amounts, key=lambda x: x.amount)
            
        elif operation == "min":
            return min(amounts, key=lambda x: x.amount)
            
        else:
            raise ValueError(f"Unsupported batch operation: {operation}")
