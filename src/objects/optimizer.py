from src.objects.truck import Truck
from src.objects.package import Package

class Optimizer:
    def __init__(self, packages, num_trucks=10, max_capacity=800):
        """
        Initierar Optimizer med paket och bilar.
        Args:
            packages (list): En lista av Package-objekt.
            num_trucks (int): Antal tillgängliga bilar.
            max_capacity (float): Maximal kapacitet per bil.
        """
        self.packages = sorted(packages, key=lambda p: (p.profit / p.weight, p.deadline), reverse=True)
        self.trucks = [Truck(truck_id=f"Truck_{i+1}", max_capacity=max_capacity) for i in range(num_trucks)]
        self.remaining_packages = []

    def distribute_packages(self):
        """Fördela paket till bilar baserat på vikt och prioritet."""
        for package in self.packages:
            placed = False
            for truck in self.trucks:
                if truck.add_package(package):
                    placed = True
                    break
            if not placed:
                self.remaining_packages.append(package)

    def calculate_total_profit(self):
        """Räkna ut total förtjänst från alla bilar."""
        return sum(truck.get_total_profit() for truck in self.trucks)

    def calculate_total_penalty(self):
        """Räkna ut totala straffavgifter från kvarvarande paket."""
        return sum(package.calculate_penalty() for package in self.remaining_packages)

    def get_summary(self):
        """Sammanställ statistik och resultat."""
        summary = {
            "total_profit": self.calculate_total_profit(),
            "total_penalty": self.calculate_total_penalty(),
            "remaining_packages": len(self.remaining_packages),
        }
        return summary

    def display_results(self):
        """Visar resultaten på ett läsbart sätt."""
        print("\n--- Resultat för Optimering ---")
        for truck in self.trucks:
            print(truck)
        print(f"\nTotalt antal paket kvar i lager: {len(self.remaining_packages)}")
        print(f"Total Förtjänst: {self.calculate_total_profit()}")
        print(f"Totala Straffavgifter: {self.calculate_total_penalty()}")
