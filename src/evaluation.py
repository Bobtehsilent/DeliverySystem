import pandas as pd
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from src.objects.package import Package
from src.optimizer import Optimizer

base_dir = os.path.abspath("..")  # En nivå upp från notebooks/
sys.path.append(base_dir)  # Lägg till base_dir i sys.path
log_file = os.path.join(base_dir, "logs", "optimization.log")

def test_optimizer(packages, test_cases):
    """Testa optimizer med olika parametrar och lagra resultaten."""
    results = []

    for case in test_cases:
        population_size = case.get("population_size", 20)
        generations = case.get("generations", 50)
        patience = case.get("patience", 5)

        optimizer = Optimizer(packages, max_trucks=10, max_capacity=800, log_file=log_file)
        stats, best_solution = optimizer.optimize(
            population_size=population_size,
            generations=generations,
            patience=patience,
        )

        # Samla resultat
        best_fitness = max(stat[1] for stat in stats)
        mean_fitness = stats[-1][2]  # Genomsnittlig fitness från sista generationen
        num_generations = len(stats)  # Hur många generationer kördes?
        results.append({
            "population_size": population_size,
            "generations": generations,
            "patience": patience,
            "best_fitness": best_fitness,
            "mean_fitness": mean_fitness,
            "num_generations": num_generations,
        })

    # Returnera resultaten som en DataFrame för analys
    return pd.DataFrame(results)

def visualize_results(results):
    """Visualisera resultat från parameter-testning med trendlinje."""
    # Best Fitness vs Population Size
    plt.figure(figsize=(10, 6))
    
    # Scatter plot for data points
    plt.scatter(results["population_size"], results["best_fitness"], color='blue', label='Data Points')
    
    # Fit a polynomial trend line (e.g., degree 2)
    z = np.polyfit(results["population_size"], results["best_fitness"], 2)
    p = np.poly1d(z)
    trendline_x = np.linspace(min(results["population_size"]), max(results["population_size"]), 100)
    trendline_y = p(trendline_x)
    
    # Plot the trend line
    plt.plot(trendline_x, trendline_y, color='red', linestyle='--', label='Trend Line (Polyfit Degree 2)')
    
    plt.xlabel("Population Size")
    plt.ylabel("Best Fitness")
    plt.title("Best Fitness vs Population Size with Trend Line")
    plt.legend()
    plt.grid(True)
    plt.show()

def analyze_best_solution(optimizer, best_solution):
    """Analysera och visualisera den bästa lösningen."""
    truck_weights = [truck.get_total_weight() for truck in optimizer.trucks]
    truck_profits = [truck.get_total_profit() for truck in optimizer.trucks]

    # Kombinera vikt och förtjänst i samma histogram
    x_labels = [f"Truck {i + 1}" for i in range(len(truck_weights))]
    x_positions = np.arange(len(truck_weights))
    width = 0.35  # Bredden för staplarna

    plt.figure(figsize=(12, 6))
    plt.bar(x_positions - width/2, truck_weights, width, label='Vikt', alpha=0.7, color='blue')
    plt.bar(x_positions + width/2, truck_profits, width, label='Förtjänst', alpha=0.7, color='orange')

    # Medelvärden
    plt.axhline(np.mean(truck_weights), color='blue', linestyle='dashed', linewidth=1, label='Medelvikt')
    plt.axhline(np.mean(truck_profits), color='orange', linestyle='dashed', linewidth=1, label='Medelförtjänst')

    # Diagraminställningar
    plt.xticks(x_positions, x_labels, rotation=45)
    plt.xlabel("Lastbilar")
    plt.ylabel("Värden")
    plt.title("Vikt och Förtjänst per Lastbil")
    plt.legend()
    plt.tight_layout()
    plt.show()

