import os
import sys
import json
import random
import time
import tracemalloc
import logging
import csv
from datetime import datetime
from plot_results import plot_results

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Adicionar o diretório raiz ao caminho de pesquisa
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from merge_sort import merge_sort
from quick_sort import quick_sort
from bubble_sort import bubble_sort
from selection_sort import selection_sort
from block_sort import block_sort
from measure_performance import measure_performance

def log_experiment_result(timestamp, alg_name, size, case, time, memory):
    log_message = f'{timestamp}", {alg_name}, {size}, {case}, {time}, {memory} MB'
    logging.info(log_message)

def measure_performance_with_progress(algorithm, arr):
    def wrapped_algorithm(arr):
        n = len(arr)
        for i in range(n):
            algorithm(arr[:i])
            if i % (n // 10) == 0 and i != 0:
                logging.info(f"Ordenação {algorithm.__name__}: {i / n:.0%} completa.")
    tracemalloc.start()
    start_time = time.time()
    wrapped_algorithm(arr)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return end_time - start_time, peak / 10**6  # Convert to MB

def run_experiment(alg_name, alg_func, sizes):
    results_dir = 'C:\\Users\\adrie\\Documents\\GitHub\\complexidade_algoritmos\\results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    results_file_json = os.path.join(results_dir, f"{alg_name}_results.json")
    all_results_file_csv = os.path.join(results_dir, "all_results.csv")
    write_header = not os.path.exists(all_results_file_csv)

    results = []

    for size in sizes:
        logging.info(f"Iniciando experimentos para {alg_name} com tamanho de entrada: {size}")

        best_case = list(range(size))  # Melhor caso: dados já ordenados
        worst_case = list(range(size, 0, -1))  # Pior caso: dados em ordem inversa
        random_cases = [random.sample(range(size), size) for _ in range(5)]  # 5 casos randômicos

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        best_time, best_memory = measure_performance_with_progress(alg_func, best_case.copy())
        log_experiment_result(timestamp, alg_name, size, "melhor", best_time, best_memory)
        result_best = {
            "timestamp": timestamp,
            "algorithm": alg_name,
            "size": size,
            "case": "melhor",
            "time": best_time,
            "memory": best_memory
        }
        results.append(result_best)

        worst_time, worst_memory = measure_performance_with_progress(alg_func, worst_case.copy())
        log_experiment_result(timestamp, alg_name, size, "pior", worst_time, worst_memory)
        result_worst = {
            "timestamp": timestamp,
            "algorithm": alg_name,
            "size": size,
            "case": "pior",
            "time": worst_time,
            "memory": worst_memory
        }
        results.append(result_worst)

        random_times = []
        random_memories = []
        for case in random_cases:
            t, m = measure_performance_with_progress(alg_func, case)
            random_times.append(t)
            random_memories.append(m)
        avg_time = sum(random_times) / len(random_times)
        avg_memory = sum(random_memories) / len(random_memories)
        log_experiment_result(timestamp, alg_name, size, "medio", avg_time, avg_memory)
        result_avg = {
            "timestamp": timestamp,
            "algorithm": alg_name,
            "size": size,
            "case": "medio",
            "time": avg_time,
            "memory": avg_memory
        }
        results.append(result_avg)

        # Salvando resultados em um único CSV (all_results.csv)
        with open(all_results_file_csv, "a", newline='') as csvfile:
            fieldnames = ["timestamp", "algorithm", "size", "case", "time", "memory"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if write_header:
                writer.writeheader()
                write_header = False

            writer.writerow(result_best)
            writer.writerow(result_worst)
            writer.writerow(result_avg)

        logging.info(f"Resultados salvos em {all_results_file_csv}")

    # Salvar resultados em JSON após todos os tamanhos serem processados
    with open(results_file_json, "w") as f:
        json.dump(results, f, indent=4)
    
    logging.info(f"Resultados salvos em {results_file_json}")

    # Após salvar todos os resultados, gerar gráficos
    plot_results(results_file_json, alg_name)
    logging.info(f"Gráficos gerados para {alg_name}")

def main():
    # Caminho absoluto para input.txt
    input_file_path = 'C:\\Users\\adrie\\Documents\\GitHub\\complexidade_algoritmos\\input.txt'

    with open(input_file_path, 'r') as file:
        lines = file.readlines()
        sizes = list(map(int, lines[0].strip().split()))
        algorithm_to_run = lines[1].strip()

    algorithms = {
        "MergeSort": merge_sort,
        "QuickSort": quick_sort,
        "BubbleSort": bubble_sort,
        "SelectionSort": selection_sort,  
        "BlockSort": block_sort
    }

    if algorithm_to_run in algorithms:
        run_experiment(algorithm_to_run, algorithms[algorithm_to_run], sizes)
    else:
        logging.error(f"Algoritmo {algorithm_to_run} não está na lista de algoritmos disponíveis.")

if __name__ == "__main__":
    main()
