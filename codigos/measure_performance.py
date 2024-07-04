import tracemalloc
import time

def measure_performance(algorithm, arr):
    tracemalloc.start()
    start_time = time.time()
    algorithm(arr)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return end_time - start_time, peak / 10**6  # Convert to MB
