from src.objects.truck import Truck
from src.objects.package import Package

class Optimizer:
    def __init__(self, packages, max_trucks=10, max_capacity=800):
        self.packages = sorted(packages, key=lambda p: (p.profit / p.weight, p.deadline), reverse=True)
        self.max_trucks = max_trucks
        self.max_capacity = max_capacity
        self.trucks = []
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

