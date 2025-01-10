import matplotlib.pyplot as plt
import numpy as np

def visualize_fitness(stats):
    """Visualisera statistik över generationer."""
    generations, best_fitness, mean_fitness = zip(*stats)
    plt.plot(generations, best_fitness, label='Bästa Fitness')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Utveckling av Fitness över Generationer')
    plt.legend()
    plt.show()

def visualize_histogram(truck_weights, truck_profits):
    """Visualisera vikt och förtjänst per lastbil i samma histogram."""
    num_trucks = len(truck_weights)
    x_labels = [f"Truck {i + 1}" for i in range(num_trucks)]
    x_positions = np.arange(num_trucks)
    width = 0.35  # Bredden för staplarna

    plt.figure(figsize=(12, 6))
    plt.bar(x_positions - width/2, truck_weights, width, label='Vikt', alpha=0.7, color='blue')
    plt.bar(x_positions + width/2, truck_profits, width, label='Förtjänst', alpha=0.7, color='orange')

    # Medelvärden
    plt.axhline(np.mean(truck_profits), color='orange', linestyle='dashed', linewidth=1, label='Medelförtjänst')

    # Diagraminställningar
    plt.xticks(x_positions, x_labels, rotation=45)
    plt.xlabel("Lastbilar")
    plt.ylabel("Värden")
    plt.title("Vikt och Förtjänst per Lastbil")
    plt.legend()
    plt.tight_layout()
    plt.show()

def visualize_logs(log_file, run_id=None):
    """Läs och visualisera loggdata från fil."""
    with open(log_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    runs = []
    current_run = []

    for line in lines:
        if "Start of Run" in line:
            current_run = []
        elif "Generation" in line:
            parts = line.split(", ")
            generation = int(parts[0].split(": ")[1])
            best_fitness = float(parts[1].split(": ")[1])
            current_run.append((generation, best_fitness))
        elif "End of Run" in line:
            if current_run:
                runs.append(current_run)

    if not runs:
        print("Inga körningar hittades i loggfilen.")
        return

    if run_id is not None:
        if run_id > len(runs) or run_id <= 0:
            print(f"Körning med ID {run_id} hittades inte. Totalt antal körningar: {len(runs)}.")
            return

        generations, best_fitness = zip(*runs[run_id - 1])
        plt.plot(generations, best_fitness, label=f'Run {run_id} Best Fitness')
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.title(f"Fitness över Generationer för Run {run_id}")
        plt.legend()
        plt.show()
    else:
        plt.figure(figsize=(10, 6))
        for i, run in enumerate(runs):
            generations, best_fitness = zip(*run)
            plt.plot(generations, best_fitness, label=f'Run {i + 1} Best Fitness')

        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.title("Fitness över Generationer för Alla Körningar")
        plt.legend()
        plt.tight_layout()
        plt.show()



