import random
import matplotlib.pyplot as plt
import numpy as np
from src.objects.truck import Truck
from src.objects.package import Package

class Optimizer:
    def __init__(self, packages, max_trucks=10, max_capacity=800, log_file="logs/optimization.log"):
        self.packages = sorted(packages, key=lambda p: (p.profit / p.weight, p.deadline), reverse=True)
        self.max_trucks = max_trucks
        self.max_capacity = max_capacity
        self.log_file = log_file

    def calculate_total_profit(self):
        """Räkna ut total förtjänst från alla bilar."""
        return sum(truck.get_total_profit() for truck in self.trucks)

    def calculate_total_penalty(self):
            """Totala straffavgifter för kvarvarande paket."""
            return sum(p.calculate_penalty() for p in self.remaining_packages)

    def initialize_population(self, population_size):
        """Skapar en initial population av lösningar."""
        population = []
        for _ in range(population_size):
            solution = []
            available_packages = self.packages[:]
            random.shuffle(available_packages)
            for _ in range(self.max_trucks):
                truck = []
                weight = 0
                while available_packages:
                    package = available_packages.pop()
                    if weight + package.weight <= self.max_capacity:
                        truck.append(package)
                        weight += package.weight
                    else:
                        break
                solution.append(truck)
            population.append(solution)
        return population

    def fitness(self, individual):
        """Beräknar fitness som total förtjänst minus straffavgifter."""
        total_profit = sum(
            sum(p.profit for p in truck_packages) for truck_packages in individual
        )
        delivered_packages = [p for truck_packages in individual for p in truck_packages]
        remaining_packages = set(self.packages) - set(delivered_packages)
        total_penalty = sum(p.calculate_penalty() for p in remaining_packages)
        return total_profit - total_penalty

    def select_parents(self, population):
        """Välj de bästa lösningarna som föräldrar."""
        population.sort(key=self.fitness, reverse=True)
        return population[:len(population) // 2]

    def crossover(self, parent1, parent2):
        """Kombinerar två lösningar till nya lösningar."""
        cut1, cut2 = sorted(random.sample(range(len(parent1)), 2))
        child1 = parent1[:cut1] + parent2[cut1:cut2] + parent1[cut2:]
        child2 = parent2[:cut1] + parent1[cut1:cut2] + parent2[cut2:]
        return child1, child2

    def mutate(self, individual, mutation_rate):
        """Muterar en lösning med en viss sannolikhet."""
        if random.random() < mutation_rate:
            truck1, truck2 = random.sample(range(len(individual)), 2)
            if individual[truck1] and individual[truck2]:
                package = individual[truck1].pop()
                if sum(p.weight for p in individual[truck2]) + package.weight <= self.max_capacity:
                    individual[truck2].append(package)
                else:
                    individual[truck1].append(package)

    def optimize(self, population_size=10, generations=50, mutation_rate=0.1):
        """Kör genetisk algoritm för optimering."""
        population = self.initialize_population(population_size)
        stats = []  # To track statistics per generation
        for generation in range(generations):
            population = self.select_parents(population)
            new_population = []
            while len(new_population) < population_size:
                parent1, parent2 = random.sample(population, 2)
                child1, child2 = self.crossover(parent1, parent2)
                self.mutate(child1, mutation_rate)
                self.mutate(child2, mutation_rate)
                new_population.extend([child1, child2])
            population = new_population[:population_size]

            # Gather stats for this generation
            best_fitness = max(self.fitness(ind) for ind in population)
            mean_fitness = np.mean([self.fitness(ind) for ind in population])
            stats.append((generation, best_fitness, mean_fitness))

            # Log generation progress
            self.log_progress(generation, best_fitness, mean_fitness)

        self.visualize_stats(stats)
        best_solution = max(population, key=self.fitness)
        self.apply_solution(best_solution)

    def apply_solution(self, solution):
        """Använd en lösning och uppdatera optimizer med jämnare fördelning."""
        self.trucks = [Truck(truck_id=f"Truck_{i + 1}", max_capacity=self.max_capacity) for i in range(self.max_trucks)]
        for i, truck_packages in enumerate(solution):
            for package in truck_packages:
                self.trucks[i].add_package(package)

    def display_results(self):
        """Visar resultaten på ett läsbart sätt."""
        total_profit = sum(truck.get_total_profit() for truck in self.trucks)
        total_penalty = sum(
            p.calculate_penalty() for truck in self.trucks for p in truck.packages
        )
        print("\n--- Resultat för Optimering ---")
        for truck in self.trucks:
            print(truck)
        print(f"\nTotalt antal paket kvar i lager: {len(self.packages) - sum(len(truck.packages) for truck in self.trucks)}")
        print(f"Total Förtjänst (levererade paket): {total_profit}")
        print(f"Totala Straffavgifter: {total_penalty}")

    def visualize_stats(self, stats):
        """Visualisera statistik över generationer."""
        generations, best_fitness, mean_fitness = zip(*stats)
        plt.plot(generations, best_fitness, label='Bästa Fitness')
        plt.plot(generations, mean_fitness, label='Genomsnittlig Fitness')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.title('Utveckling av Fitness över Generationer')
        plt.legend()
        plt.show()

    def analyze_solution(self):
        """Analysera och visualisera fördelningen av vikt och förtjänst."""
        truck_weights = [truck.get_total_weight() for truck in self.trucks]
        truck_profits = [truck.get_total_profit() for truck in self.trucks]
        
        # Histogram för vikt och förtjänst
        plt.hist(truck_weights, bins=10, alpha=0.7, label='Vikt')
        plt.hist(truck_profits, bins=10, alpha=0.7, label='Förtjänst')
        plt.xlabel('Värde')
        plt.ylabel('Antal Lastbilar')
        plt.title('Histogram för Vikt och Förtjänst')
        plt.legend()
        plt.show()

        # Statistik
        print("--- Statistik för Lastbilar ---")
        print(f"Medelvikt: {np.mean(truck_weights):.2f}, Varians: {np.var(truck_weights):.2f}, Std Avvikelse: {np.std(truck_weights):.2f}")
        print(f"Medelförtjänst: {np.mean(truck_profits):.2f}, Varians: {np.var(truck_profits):.2f}, Std Avvikelse: {np.std(truck_profits):.2f}")


    def reset(self):
        """Återställ optimizer till ursprungligt tillstånd."""
        self.trucks = []
        self.remaining_packages = []

    def log_progress(self, generation, best_fitness, mean_fitness):
        """Logga varje generations framgångar."""
        log_message = (
            f"Generation: {generation}, "
            f"Best Fitness: {best_fitness:.2f}, "
            f"Mean Fitness: {mean_fitness:.2f}\n"
        )
        with open(self.log_file, "a", encoding="utf-8") as log_file:
            log_file.write(log_message)

    def export_truck_details(self, file_name="truck_details.txt"):
        """Exportera detaljer om varje lastbil och dess paket till en textfil."""
        with open(file_name, "w", encoding="utf-8") as file:
            for truck in self.trucks:
                file.write(f"Truck ID: {truck.id}\n")
                file.write(f"Total Weight: {truck.get_total_weight()}\n")
                file.write(f"Total Profit: {truck.get_total_profit()}\n")
                file.write(f"Total Penalty: {sum(p.calculate_penalty() for p in truck.packages)}\n")
                file.write(f"Packages: {len(truck.packages)}\n")
                file.write(f"{'Package ID':<15}{'Weight':<15}{'Profit':<15}{'Deadline':<15}\n")
                file.write("-" * 60 + "\n")
                for package in truck.packages:
                    file.write(f"{package.id:<15}{package.weight:<15.2f}{package.profit:<15.2f}{package.deadline:<15}\n")
                file.write("\n")

