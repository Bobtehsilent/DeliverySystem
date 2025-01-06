class Truck:
    def __init__(self, truck_id:int, max_capacity:int=800):
        self.id = truck_id
        self.max_capacity = max_capacity
        self.packages = []

    def add_package(self, package):
        """Lägg till ett paket om det finns plats."""
        if self.get_total_weight() + package.weight <= self.max_capacity:
            self.packages.append(package)
            return True
        return False
    
    def get_total_weight(self):
        """Beräknar totala vikten för paketen i bilen"""
        return sum([p.weight for p in self.packages])
    
    def get_total_profit(self):
        """Totala förtjänsten inklusive straffavgifter."""
        total_profit = sum(p.effective_profit() for p in self.packages)
        return total_profit
    
    def __repr__(self):
        return f"Truck({self.id}, Total Weight: {self.get_total_weight()}, Packages: {len(self.packages)})"