from rich.console import Console
from rich.table import Table
from centinel import Money, Currency, convert, AdvancedOperations

console = Console()

def demonstrate_basic_operations():
    console.print("\n[bold green]Basic Money Operations[/bold green]")
    
    # Create money objects
    m1 = Money(100, Currency.USD)
    m2 = Money(50, Currency.USD)
    
    # Addition
    result = m1 + m2
    console.print(f"Addition: {m1} + {m2} = {result}")
    
    # Subtraction
    result = m1 - m2
    console.print(f"Subtraction: {m1} - {m2} = {result}")
    
    # Multiplication
    result = m1 * 2
    console.print(f"Multiplication: {m1} * 2 = {result}")
    
    # Division
    result = m1 / 2
    console.print(f"Division: {m1} / 2 = {result}")

def demonstrate_currency_conversion():
    console.print("\n[bold green]Currency Conversion[/bold green]")
    
    amount = Money(100, Currency.USD)
    table = Table(title="Currency Conversion Examples")
    
    table.add_column("From", style="cyan")
    table.add_column("To", style="magenta")
    table.add_column("Result", style="green")
    
    for currency in Currency:
        if currency != Currency.USD:
            converted = convert(amount, currency)
            table.add_row(str(amount), currency.value, str(converted))
    
    console.print(table)

def demonstrate_advanced_operations():
    console.print("\n[bold green]Advanced Financial Operations[/bold green]")
    
    # Compound Interest
    principal = Money(1000, Currency.USD)
    result = AdvancedOperations.compound_interest(principal, 0.05, 1)
    console.print(f"Compound Interest (5% for 1 year): {principal} → {result}")
    
    # Percentage Calculation
    amount = Money(200, Currency.USD)
    percentage_result = AdvancedOperations.percentage_of(amount, 15)
    console.print(f"15% of {amount} = {percentage_result}")
    
    # Financial Ratios
    revenue = Money(1000, Currency.USD)
    costs = Money(600, Currency.USD)
    margin = AdvancedOperations.profit_margin(revenue, costs)
    console.print(f"\nProfit Margin: {margin:.2%}")
    
    debt = Money(500, Currency.USD)
    equity = Money(1000, Currency.USD)
    ratio = AdvancedOperations.debt_to_equity(debt, equity)
    console.print(f"Debt to Equity Ratio: {ratio:.2f}")
    
    # Batch Operations
    amounts = [
        Money(100, Currency.USD),
        Money(200, Currency.USD),
        Money(300, Currency.USD)
    ]
    console.print("\nBatch Operations:")
    operations = ["sum", "average", "max", "min"]
    for op in operations:
        result = AdvancedOperations.batch_operation(amounts, op)
        console.print(f"{op.capitalize()}: {result}")

if __name__ == "__main__":
    console.print("[bold]Financial Library Examples[/bold]")
    demonstrate_basic_operations()
    demonstrate_currency_conversion()
    demonstrate_advanced_operations()
