from rich.console import Console
from rich.table import Table
import time
import concurrent.futures
from centinel import (
    Money, Currency, OptimizedMoney, BatchProcessor,
    cached_exchange_rate
)

console = Console()

def benchmark_operations():
    console.print("\n[bold green]Performance Benchmarks[/bold green]")
    
    # Setup test data with larger dataset
    n_operations = 100000
    amounts = [Money(100, Currency.USD) for _ in range(n_operations)]
    
    # Test regular operations
    start_time = time.perf_counter()
    result = amounts[0]
    for amount in amounts[1:]:
        result += amount
    regular_time = time.perf_counter() - start_time
    
    # Test optimized operations
    processor = BatchProcessor()
    start_time = time.perf_counter()
    optimized_result = processor.batch_add(amounts)
    optimized_time = time.perf_counter() - start_time
    
    # Test concurrent batch operations
    def process_batch(batch):
        return processor.batch_add(batch)
    
    start_time = time.perf_counter()
    batch_size = 10000
    batches = [amounts[i:i + batch_size] for i in range(0, len(amounts), batch_size)]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        partial_results = list(executor.map(process_batch, batches))
    
    concurrent_result = processor.batch_add(partial_results)
    concurrent_time = time.perf_counter() - start_time
    
    # Display results
    table = Table(title=f"Performance Comparison ({n_operations} operations)")
    table.add_column("Operation Type", style="cyan")
    table.add_column("Time (seconds)", style="magenta")
    table.add_column("Result", style="green")
    
    table.add_row(
        "Regular Addition",
        f"{regular_time:.4f}",
        str(result)
    )
    table.add_row(
        "Optimized Addition",
        f"{optimized_time:.4f}",
        str(optimized_result)
    )
    table.add_row(
        "Concurrent Batch Addition",
        f"{concurrent_time:.4f}",
        str(concurrent_result)
    )
    
    console.print(table)
    
    # Show detailed metrics
    metrics = processor.get_performance_metrics()
    console.print("\n[bold]Detailed Performance Metrics[/bold]")
    for operation, stats in metrics.items():
        console.print(f"\n{operation}:")
        for metric, value in stats.items():
            if metric.endswith('time'):
                console.print(f"  {metric}: {value:.6f} seconds")
            else:
                console.print(f"  {metric}: {value}")

    # Test exchange rate caching
    console.print("\n[bold]Exchange Rate Cache Performance[/bold]")
    start_time = time.perf_counter()
    for _ in range(10000):
        cached_exchange_rate(Currency.USD, Currency.EUR)
    cache_time = time.perf_counter() - start_time
    console.print(f"Time for 10000 cached rate lookups: {cache_time:.6f} seconds")

if __name__ == "__main__":
    console.print("[bold]Financial Library Performance Tests[/bold]")
    benchmark_operations()
