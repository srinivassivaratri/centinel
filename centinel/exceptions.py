class MoneyOverflowError(OverflowError):
    """Raised when a monetary calculation would exceed the 4-byte integer limit."""
    pass

class InvalidAmountError(ValueError):
    """Raised when an invalid monetary amount is provided."""
    pass

class CurrencyMismatchError(ValueError):
    """Raised when attempting operations between different currencies."""
    pass
