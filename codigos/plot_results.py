import matplotlib.pyplot as plt
import json
import os

def plot_results(filename, title_prefix):
    with open(filename) as f:
        results = json.load(f)

    sizes = sorted(set(entry["size"] for entry in results))
    
    best_times = []
    worst_times = []
    avg_times = []

    best_memory = []
    worst_memory = []
    avg_memory = []

    for size in sizes:
        best_case = next(entry for entry in results if entry["size"] == size and entry["case"] == "melhor")
        worst_case = next(entry for entry in results if entry["size"] == size and entry["case"] == "pior")
        avg_case = next(entry for entry in results if entry["size"] == size and entry["case"] == "medio")

        best_times.append(best_case["time"])
        worst_times.append(worst_case["time"])
        avg_times.append(avg_case["time"])

        best_memory.append(best_case["memory"])
        worst_memory.append(worst_case["memory"])
        avg_memory.append(avg_case["memory"])

    plt.figure(figsize=(12, 6))
    plt.plot(sizes, best_times, label="Best Case Time")
    plt.plot(sizes, worst_times, label="Worst Case Time")
    plt.plot(sizes, avg_times, label="Average Case Time")
    plt.xlabel("Input Size")
    plt.ylabel("Time (seconds)")
    plt.title(f"{title_prefix} Time Complexity")
    plt.legend()
    plt.grid(True)
    plot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plots')
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    plt.savefig(os.path.join(plot_dir, f"{title_prefix}_time_plot.png"))
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.plot(sizes, best_memory, label="Best Case Memory")
    plt.plot(sizes, worst_memory, label="Worst Case Memory")
    plt.plot(sizes, avg_memory, label="Average Case Memory")
    plt.xlabel("Input Size")
    plt.ylabel("Memory (MB)")
    plt.title(f"{title_prefix} Memory Usage")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(plot_dir, f"{title_prefix}_memory_plot.png"))
    plt.show()
