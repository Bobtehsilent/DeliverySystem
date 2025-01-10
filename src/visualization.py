import matplotlib.pyplot as plt
import os
import numpy as np

def visualize_fitness(stats, result_dir=None):
    """Visualisera fitness score över generationer."""
    generations, best_fitness, mean_fitness = zip(*stats)

    plt.figure(figsize=(10, 6))

    plt.plot(generations, best_fitness, label="Best Fitness", color="green")
    plt.plot(generations, mean_fitness, label="Mean Fitness", color="blue")

    for gen, best, mean in zip(generations, best_fitness, mean_fitness):
        plt.plot([gen, gen], [mean, best], color="red", linestyle="dotted", linewidth=0.8)

    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Fitness Evolution Over Generations")
    plt.legend()
    plt.tight_layout()

    if result_dir:
        file_path = os.path.join(result_dir, "fitness_evolution.png")
        plt.savefig(file_path)
        print(f"Fitness evolution saved to {file_path}")
        plt.close()
    else:
        plt.show()

def leftover_histogram(trucks, packages, result_dir=None):
    """Skapa och spara histogram för vikter och förtjänster för kvarvarande paket."""
    delivered_packages = {p for truck in trucks for p in truck.packages}
    leftover_packages = [p for p in packages if p not in delivered_packages]

    if not leftover_packages:
        print("No leftover packages to visualize.")
        return

    leftover_weights = [p.weight for p in leftover_packages]
    leftover_profits = [p.profit for p in leftover_packages]

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.hist(leftover_weights, bins=10, alpha=0.7, color="lightblue")
    plt.axvline(
        np.mean(leftover_weights),
        color="red",
        linestyle="dashed",
        linewidth=1,
        label=f"Mean: {np.mean(leftover_weights):.2f}",
    )
    plt.axvline(
        np.mean(leftover_weights) + np.std(leftover_weights),
        color="green",
        linestyle="dashed",
        linewidth=1,
        label=f"Std Dev: ±{np.std(leftover_weights):.2f}",
    )
    plt.axvline(
        np.mean(leftover_weights) - np.std(leftover_weights),
        color="green",
        linestyle="dashed",
        linewidth=1,
    )
    plt.xlabel("Weight")
    plt.ylabel("Frequency")
    plt.title("Leftover Package Weights")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.hist(leftover_profits, bins=10, alpha=0.7, color="lightgreen")
    plt.axvline(
        np.mean(leftover_profits),
        color="red",
        linestyle="dashed",
        linewidth=1,
        label=f"Mean: {np.mean(leftover_profits):.2f}",
    )
    plt.axvline(
        np.mean(leftover_profits) + np.std(leftover_profits),
        color="blue",
        linestyle="dashed",
        linewidth=1,
        label=f"Std Dev: ±{np.std(leftover_profits):.2f}",
    )
    plt.axvline(
        np.mean(leftover_profits) - np.std(leftover_profits),
        color="blue",
        linestyle="dashed",
        linewidth=1,
    )
    plt.xlabel("Profit")
    plt.ylabel("Frequency")
    plt.title("Leftover Package Profits")
    plt.legend()

    plt.tight_layout()

    # Sparar enbart om result_dir är angivet annars visas det direkt
    if result_dir:
        filepath = os.path.join(result_dir, "leftover_distribution.png")
        plt.savefig(filepath)
        print(f"Leftover histograms saved to {filepath}")
        plt.close()
    else:
        print("Displaying leftover histograms...")
        plt.show()

def visualize_histogram(truck_weights, truck_profits, result_dir=None):
    """Visualisera histogram för vikter och förtjänster per lastbil."""
    num_trucks = len(truck_weights)
    x_labels = [f"Truck {i + 1}" for i in range(num_trucks)]
    x_positions = np.arange(num_trucks)
    width = 0.35 

    plt.figure(figsize=(12, 6))
    
    plt.bar(x_positions - width / 2, truck_weights, width, label="Weight", alpha=0.7, color="lightblue")
    plt.bar(x_positions + width / 2, truck_profits, width, label="Profit", alpha=0.7, color="lightgreen")

    mean_profit = np.mean(truck_profits)
    std_profit = np.std(truck_profits)
    plt.axhline(mean_profit, color="blue", linestyle="dashed", linewidth=1.5, label=f"Avg Profit: {mean_profit:.2f}")
    plt.axhline(mean_profit + std_profit, color="blue", linestyle="dotted", linewidth=1.2, label=f"Profit Std Dev: ±{std_profit:.2f}")
    plt.axhline(mean_profit - std_profit, color="blue", linestyle="dotted", linewidth=1.2)

    mean_weight = np.mean(truck_weights)
    std_weight = np.std(truck_weights)
    plt.axhline(mean_weight, color="green", linestyle="dashed", linewidth=1.5, label=f"Avg Weight: {mean_weight:.2f}")
    plt.axhline(mean_weight + std_weight, color="green", linestyle="dotted", linewidth=1.2, label=f"Weight Std Dev: ±{std_weight:.2f}")
    plt.axhline(mean_weight - std_weight, color="green", linestyle="dotted", linewidth=1.2)

    plt.xticks(x_positions, x_labels, rotation=45)
    plt.xlabel("Trucks")
    plt.ylabel("Values")
    plt.title("Weight and Profit per Truck")
    plt.legend()
    plt.tight_layout()

    # Sparar enbart om result_dir är angivet annars visas det direkt
    if result_dir:
        file_path = os.path.join(result_dir, "truck_distribution.png")
        plt.savefig(file_path)
        print(f"Truck distribution histogram saved to {file_path}")
        plt.close()
    else:
        plt.show()

"""En idé att visualisera logsen men insåg att det inte var nödvändigt"""

# def visualize_logs(log_file, run_id=None):
#     """Läs och visualisera loggdata från fil."""
#     with open(log_file, "r", encoding="utf-8") as file:
#         lines = file.readlines()

#     runs = []
#     current_run = []

#     for line in lines:
#         if "Start of Run" in line:
#             current_run = []
#         elif "Generation" in line:
#             parts = line.split(", ")
#             generation = int(parts[0].split(": ")[1])
#             best_fitness = float(parts[1].split(": ")[1])
#             current_run.append((generation, best_fitness))
#         elif "End of Run" in line:
#             if current_run:
#                 runs.append(current_run)

#     if not runs:
#         print("Inga körningar hittades i loggfilen.")
#         return

#     if run_id is not None:
#         if run_id > len(runs) or run_id <= 0:
#             print(f"Körning med ID {run_id} hittades inte. Totalt antal körningar: {len(runs)}.")
#             return

#         generations, best_fitness = zip(*runs[run_id - 1])
#         plt.plot(generations, best_fitness, label=f'Run {run_id} Best Fitness')
#         plt.xlabel("Generation")
#         plt.ylabel("Fitness")
#         plt.title(f"Fitness över Generationer för Run {run_id}")
#         plt.legend()
#         plt.show()
#     else:
#         plt.figure(figsize=(10, 6))
#         for i, run in enumerate(runs):
#             generations, best_fitness = zip(*run)
#             plt.plot(generations, best_fitness, label=f'Run {i + 1} Best Fitness')

#         plt.xlabel("Generation")
#         plt.ylabel("Fitness")
#         plt.title("Fitness över Generationer för Alla Körningar")
#         plt.legend()
#         plt.tight_layout()
#         plt.show()



