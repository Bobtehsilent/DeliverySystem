from src.objects.truck import Truck
import random
from src.objects.package import Package

class Optimizer:
    def __init__(self, packages, max_trucks=10, max_capacity=800, log_file="logs/optimization.log"):
        self.packages = sorted(packages, key=lambda p: (p.profit / p.weight, p.deadline), reverse=True)
        self.max_trucks = max_trucks
        self.max_capacity = max_capacity
        self.trucks = []
        self.remaining_packages = []
        self.log_file = log_file


    def distribute_packages(self):
        """Fördela paket till bilar baserat på vikt och prioritet."""
        for package in self.packages:
            placed = False
            for truck in self.trucks:
                if truck.add_package(package):
                    placed = True
                    break
            
            if not placed:
                if len(self.trucks) < self.max_trucks:
                    new_truck = Truck(truck_id=f"Truck_{len(self.trucks) + 1}", max_capacity=self.max_capacity)
                    if new_truck.add_package(package):
                        self.trucks.append(new_truck)
                    else:
                        self.remaining_packages.append(package)
                else:
                    # Om max antal bilar är nått, lägg paketet i lager
                    self.remaining_packages.append(package)

        print(f"Total remaining packages in storage: {len(self.remaining_packages)}")


    def calculate_total_profit(self):
        """Räkna ut total förtjänst från alla bilar."""
        return sum(truck.get_total_profit() for truck in self.trucks)

    def calculate_total_penalty(self):
        """Totala straffavgifter för både levererade och ej levererade paket."""
        delivered_penalties = sum(
            p.calculate_penalty() for truck in self.trucks for p in truck.packages
        )
        remaining_penalties = sum(p.calculate_penalty() for p in self.remaining_packages)
        return delivered_penalties + remaining_penalties

    def get_summary(self):
        """Sammanställ statistik och resultat."""
        summary = {
            "total_profit": self.calculate_total_profit(),
            "total_penalty": self.calculate_total_penalty(),
            "remaining_packages": len(self.remaining_packages),
            "used_trucks": len(self.trucks),
        }
        return summary

    def display_results(self):
        """Visar resultaten på ett läsbart sätt."""
        summary = self.get_summary()
        print("\n--- Resultat för Optimering ---")
        for truck in self.trucks:
            print(truck)
        print(f"\nTotalt antal paket kvar i lager: {summary['remaining_packages']}")
        print(f"Total Förtjänst (levererade paket): {summary['total_profit']}")
        print(f"Totala Straffavgifter: {summary['total_penalty']}")
        print(f"Använda bilar: {summary['used_trucks']}")

##############################################################################################################
### OPTIMERINGSMETODER - GREEDY OCH GENETIC
##############################################################################################################
    
    def greedy_optimization(self):
        """Baseline greedy-algoritm som optimerar förtjänst."""
        for package in self.packages:
            placed = False
            for truck in self.trucks:
                if truck.add_package(package):
                    placed = True
                    break
            
            if not placed and len(self.trucks) < self.max_trucks:
                new_truck = Truck(truck_id=f"Truck_{len(self.trucks) + 1}", max_capacity=self.max_capacity)
                new_truck.add_package(package)
                self.trucks.append(new_truck)
            elif not placed:
                self.remaining_packages.append(package)

        self.log_progress(iteration=0)

    def genetic_optimization(self, population_size=10, generations=50, mutation_rate=0.1):
        """Genetisk algoritm för att optimera lösningen."""
        population = self.initialize_population(population_size)

        for generation in range(1, generations + 1):
            fitness_scores = [(individual, self.fitness(individual)) for individual in population]
            fitness_scores.sort(key=lambda x: x[1], reverse=True)  # Sortera efter fitness

            top_individuals = [ind[0] for ind in fitness_scores[:population_size // 2]]

            new_population = top_individuals[:]
            while len(new_population) < population_size:
                parent1, parent2 = random.sample(top_individuals, 2)
                child1, child2 = self.crossover(parent1, parent2)
                self.mutate(child1, mutation_rate)
                self.mutate(child2, mutation_rate)
                new_population.extend([child1, child2])

            population = new_population[:population_size]
            self.log_progress(iteration=generation, fitness_scores=fitness_scores)  # Logga förbättringar

        # Bästa lösning
        best_solution = fitness_scores[0][0]
        self.apply_solution(best_solution)


    def initialize_population(self, population_size):
        """Skapar en initial population"""
        population = []
        for _ in range(population_size):
            random.shuffle(self.packages)
            solution = [self.packages[i::self.max_trucks] for i in range(self.max_trucks)]
            population.append(solution)
        return population
    
    def fitness(self, individual):
        """Beräkna fitness för en lösning."""
        total_profit = 0
        total_penalty = 0
        for truck_packages in individual:
            truck = Truck(truck_id="temp", max_capacity=self.max_capacity)
            for package in truck_packages:
                if truck.add_package(package):
                    total_profit += package.effective_profit()
                else:
                    total_penalty += package.calculate_penalty()
        return total_profit + total_penalty

    def crossover(self, parent1, parent2):
        """Utför crossover mellan två föräldrar."""
        cut = random.randint(1, len(parent1) - 1)
        child1 = parent1[:cut] + parent2[cut:]
        child2 = parent2[:cut] + parent1[cut:]
        return child1, child2
    
    def mutate(self, individual, mutation_rate):
        """Mutera en lösning med en viss sannolikhet."""
        for truck_packages in individual:
            if random.random() < mutation_rate:
                idx1, idx2 = random.sample(range(len(truck_packages)), 2)
                truck_packages[idx1], truck_packages[idx2] = truck_packages[idx2], truck_packages[idx1]

    def apply_solution(self, solution):
        """Använd en lösning för att uppdatera bilar och paket."""
        self.trucks = [Truck(truck_id=f"Truck_{i + 1}", max_capacity=self.max_capacity) for i in range(len(solution))]
        self.remaining_packages = []
        for i, truck_packages in enumerate(solution):
            for package in truck_packages:
                if not self.trucks[i].add_package(package):
                    self.remaining_packages.append(package)

    def log_progress(self, iteration, fitness_scores=None):
        """Logga framsteg i optimeringsalgoritmen."""
        total_profit = self.calculate_total_profit()
        total_penalty = self.calculate_total_penalty()
        score = total_profit + total_penalty
        remaining_packages = len(self.remaining_packages)
        used_trucks = len(self.trucks)

        if fitness_scores:
            best_fitness = max(score for _, score in fitness_scores)
        else:
            best_fitness = "N/A"

        log_message = (
            f"Iteration: {iteration}, "
            f"Fitness Score: {best_fitness}, "
            f"Score: {score}, "
            f"Total Profit: {total_profit}, "
            f"Total Penalty: {total_penalty}, "
            f"Remaining Packages: {remaining_packages}, "
            f"Used Trucks: {used_trucks}\n"
        )

        with open(self.log_file, "a", encoding="latin1") as log_file:  # Ändrad kodning
            log_file.write(log_message)


