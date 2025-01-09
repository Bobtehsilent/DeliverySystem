import matplotlib.pyplot as plt
import numpy as np

def visualize_fitness(stats):
    """Visualisera statistik över generationer."""
    generations, best_fitness, mean_fitness = zip(*stats)
    plt.plot(generations, best_fitness, label='Bästa Fitness')
    plt.plot(generations, mean_fitness, label='Genomsnittlig Fitness')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Utveckling av Fitness över Generationer')
    plt.legend()
    plt.show()

def visualize_histogram(truck_weights, truck_profits):
    """Visualisera vikt och förtjänst per lastbil med medelvärde och standardavvikelse."""
    num_trucks = len(truck_weights)
    x_labels = [f"Truck {i + 1}" for i in range(num_trucks)]
    x_positions = np.arange(num_trucks)

    # Vikt
    plt.bar(x_positions, truck_weights, alpha=0.7, label='Vikt')
    plt.axhline(np.mean(truck_weights), color='r', linestyle='dashed', linewidth=1, label='Mean Vikt')
    plt.axhline(np.mean(truck_weights) + np.std(truck_weights), color='g', linestyle='dashed', linewidth=1, label='Std Dev Vikt')
    plt.axhline(np.mean(truck_weights) - np.std(truck_weights), color='g', linestyle='dashed', linewidth=1)
    plt.xticks(x_positions, x_labels, rotation=45, ha='right')
    plt.xlabel('Lastbilar')
    plt.ylabel('Vikt')
    plt.title('Vikt per Lastbil')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Förtjänst
    plt.bar(x_positions, truck_profits, alpha=0.7, label='Förtjänst', color='orange')
    plt.axhline(np.mean(truck_profits), color='r', linestyle='dashed', linewidth=1, label='Mean Förtjänst')
    plt.axhline(np.mean(truck_profits) + np.std(truck_profits), color='g', linestyle='dashed', linewidth=1, label='Std Dev Förtjänst')
    plt.axhline(np.mean(truck_profits) - np.std(truck_profits), color='g', linestyle='dashed', linewidth=1)
    plt.xticks(x_positions, x_labels, rotation=45, ha='right')
    plt.xlabel('Lastbilar')
    plt.ylabel('Förtjänst')
    plt.title('Förtjänst per Lastbil')
    plt.legend()
    plt.tight_layout()
    plt.show()


def log_fitness_trends(log_file):
    """Läs och visualisera fitness-data från loggfilen."""
    generations = []
    best_fitness = []
    mean_fitness = []

    with open(log_file, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(", ")
            generation = int(parts[0].split(": ")[1])
            best = float(parts[1].split(": ")[1])
            mean = float(parts[2].split(": ")[1])
            generations.append(generation)
            best_fitness.append(best)
            mean_fitness.append(mean)

    plt.plot(generations, best_fitness, label='Bästa Fitness')
    plt.plot(generations, mean_fitness, label='Genomsnittlig Fitness')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Utveckling av Fitness från Loggfil')
    plt.legend()
    plt.show()
