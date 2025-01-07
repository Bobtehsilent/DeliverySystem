class Package:
    def __init__(self, package_id:int, weight:float, profit:int, deadline:int):
        self.id = package_id
        self.weight = weight
        self.profit = profit
        self.deadline = deadline

    def calculate_penalty(self):
        """Beräknar straffavgiften för leveransförsening"""
        if self.deadline < 0:
            return -(self.deadline ** 2)
        return 0
    
    def effective_profit(self):
        """Beräknar effektiv förtjänst efter straffavgift"""
        penalty = self.calculate_penalty()
        effective = self.profit + penalty
        return effective
    
    def priority_score(self):
        """Beräkna ett prioriteringsvärde för paket baserat på profit, vikt och deadline."""
        if self.deadline < 0: 
            lateness_factor = 2
        elif self.deadline == 0:
            lateness_factor = 1.5
        else:
            lateness_factor = 1

        return (self.profit / self.weight) * lateness_factor

    def __repr__(self):
            return f"Package({self.id}, Weight: {self.weight}, Profit: {self.profit}, Deadline: {self.deadline})"