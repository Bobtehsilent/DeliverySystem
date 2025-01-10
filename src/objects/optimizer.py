import random
import matplotlib.pyplot as plt
import numpy as np
from src.objects.truck import Truck
from src.objects.package import Package
from src.visualization import visualize_histogram, visualize_fitness
import os
import sys
import time

base_dir = os.path.abspath("..") 
sys.path.append(base_dir)  
log_file = os.path.join(base_dir, "logs", "optimization.log")
class Optimizer:
    def __init__(self, packages, max_trucks=10, max_capacity=800, log_file=log_file):
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
        """Skapar en initial population med mer slumpmässighet."""
        population = []
        for _ in range(population_size):
            solution = []
            available_packages = self.packages[:]
            random.shuffle(available_packages)  # Slumpmässig start
            for _ in range(self.max_trucks):
                truck = []
                weight = 0
                while available_packages:
                    package = random.choice(available_packages)  # Välj ett slumpmässigt paket
                    if weight + package.weight <= self.max_capacity:
                        truck.append(package)
                        weight += package.weight
                        available_packages.remove(package)
                    else:
                        break
                solution.append(truck)
            population.append(solution)
        return population

    def fitness(self, individual):
        """Beräknar fitness med en diversitetskomponent."""
        total_profit = sum(
            sum(p.profit for p in truck_packages) for truck_packages in individual
        )
        delivered_packages = [p for truck_packages in individual for p in truck_packages]
        remaining_packages = set(self.packages) - set(delivered_packages)
        total_penalty = sum(p.calculate_penalty() for p in remaining_packages)

        # Diversitetskomponent: straffa lösningar där samma paket används ofta
        diversity_score = len(set(delivered_packages)) / len(delivered_packages) if delivered_packages else 0

        return (total_profit - total_penalty + 0.1 * diversity_score)  # Justera faktorn 0.1 vid behov

    def select_parents(self, population):
        """Välj föräldrar med turneringsmetod för lägre selektionspress."""
        tournament_size = 5  # Öka storleken för att minska selektionspressen
        parents = []
        for _ in range(len(population) // 2):
            candidates = random.sample(population, tournament_size)
            parent = max(candidates, key=self.fitness)
            parents.append(parent)
        return parents

    def crossover(self, parent1, parent2):
        """Kombinerar föräldrar och säkerställer att paket inte dupliceras."""
        child1, child2 = [], []
        used_packages_child1 = set()
        used_packages_child2 = set()

        for truck1, truck2 in zip(parent1, parent2):
            combined = truck1 + truck2  # Kombinera paket från båda föräldrarna
            random.shuffle(combined)  # Introducera slumpmässighet

            # Fyll barnens lastbilar baserat på kapacitet
            truck_child1, truck_child2 = [], []
            weight1, weight2 = 0, 0

            for package in combined:
                if package in used_packages_child1 or package in used_packages_child2:
                    continue  # Hoppa över paket som redan har använts
                if weight1 + package.weight <= self.max_capacity:
                    truck_child1.append(package)
                    weight1 += package.weight
                    used_packages_child1.add(package)
                elif weight2 + package.weight <= self.max_capacity:
                    truck_child2.append(package)
                    weight2 += package.weight
                    used_packages_child2.add(package)

            child1.append(truck_child1)
            child2.append(truck_child2)

        return child1, child2

    def mutate(self, individual, mutation_rate):
        """Muterar en lösning för att öka variationen."""
        if random.random() < mutation_rate:
            truck1, truck2 = random.sample(range(len(individual)), 2)
            if individual[truck1] and individual[truck2]:
                # Flytta ett paket mellan två lastbilar
                package = individual[truck1].pop(random.randint(0, len(individual[truck1]) - 1))
                if sum(p.weight for p in individual[truck2]) + package.weight <= self.max_capacity:
                    individual[truck2].append(package)
                else:
                    individual[truck1].append(package)
        # Introducera slumpmässig omfördelning av paket inom en lastbil
        for truck_packages in individual:
            if random.random() < mutation_rate:
                random.shuffle(truck_packages)

    def optimize(self, population_size=10, generations=50, initial_mutation_rate=0.05, patience=5, mutation_increase=0.05):
        """Genetisk algoritm med elitism och stoppkriterium för stagnation och dynamisk mutation."""
        run_id = random.randint(1, 9999)  # Generera unikt run_id här
        population = self.initialize_population(population_size)
        stats = []
        best_solution = None
        stagnation_counter = 0  # Räknare för generationer utan förbättring
        last_best_fitness = None  # Senast observerade bästa fitness
        last_mean_fitness = None  # Senast observerade genomsnittliga fitness
        mutation_rate = initial_mutation_rate  # Startvärde för mutation rate

        for generation in range(generations):
            population = self.select_parents(population)
            new_population = population[:2]  # Elitism: Behåll de två bästa
            while len(new_population) < population_size:
                parent1, parent2 = random.sample(population, 2)
                child1, child2 = self.crossover(parent1, parent2)
                self.mutate(child1, mutation_rate)
                self.mutate(child2, mutation_rate)
                new_population.extend([child1, child2])
            population = new_population[:population_size]

            # Beräkna fitness
            best_fitness = max(self.fitness(ind) for ind in population)
            mean_fitness = np.mean([self.fitness(ind) for ind in population])
            stats.append((generation, best_fitness, mean_fitness))

            # Logga framgång
            self.log_progress(generation, best_fitness, mean_fitness, run_id=run_id)

            # Kontrollera om fitness har stagnerat
            if best_fitness == last_best_fitness:
                stagnation_counter += 1
                if stagnation_counter >= patience:
                    mutation_rate += mutation_increase  # Öka mutation rate
                    stagnation_counter = 0  # Återställ räknaren
            else:
                stagnation_counter = 0  # Återställ räknaren vid förbättring
                mutation_rate = initial_mutation_rate  # Återställ mutation rate vid förändring

            last_best_fitness = best_fitness
            last_mean_fitness = mean_fitness

            # Stoppkriterium: Avbryt om maximal generationsgräns uppnås
            if stagnation_counter >= patience:
                print(f"Optimeringen stoppas vid generation {generation} efter {patience} generationer av stagnation.")
                break

        # Hitta och applicera bästa lösningen
        best_solution = max(population, key=self.fitness)
        self.apply_solution(best_solution)

        # Logga slutet av körningen
        self.log_progress(-1, best_fitness, mean_fitness, run_id=run_id)

        return stats, best_solution

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
        print(f"Actual total profit: {total_profit + total_penalty}")

    def log_progress(self, generation, best_fitness, mean_fitness, run_id):
        """Logga varje generations framgångar med löpande körnings-ID."""
        # Om första generationen, lägg till en separator
        if generation == 0:
            header = f"\n{'=' * 20} Start of Run {run_id} {'=' * 20}\n"
            with open(self.log_file, "a", encoding="utf-8") as log_file:
                log_file.write(header)

        # Logga varje generation
        if generation >= 0:
            log_message = (
                f"Generation: {generation}, "
                f"Best Fitness: {best_fitness:.2f}, "
                f"Mean Fitness: {mean_fitness:.2f}\n"
            )
            with open(self.log_file, "a", encoding="utf-8") as log_file:
                log_file.write(log_message)

        # Vid slutet av körningen, skriv en slutlig separator
        if generation == -1:  # Indikera slutet av körningen
            footer = f"{'=' * 20} End of Run {run_id} {'=' * 20}\n"
            with open(self.log_file, "a", encoding="utf-8") as log_file:
                log_file.write(footer)


    def analyze_solution(self):
        """Analysera och visualisera fördelningen av vikt och förtjänst."""
        truck_weights = [truck.get_total_weight() for truck in self.trucks]
        truck_profits = [truck.get_total_profit() for truck in self.trucks]

        visualize_histogram(truck_weights, truck_profits)

        print("--- Statistik för Lastbilar ---")
        print(f"Medelvikt: {np.mean(truck_weights):.2f}, Varians: {np.var(truck_weights):.2f}, Std Avvikelse: {np.std(truck_weights):.2f}")
        print(f"Medelförtjänst: {np.mean(truck_profits):.2f}, Varians: {np.var(truck_profits):.2f}, Std Avvikelse: {np.std(truck_profits):.2f}")

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

