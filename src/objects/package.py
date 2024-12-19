class Package:
    def __init__(self, package_id:int, weight:float, profit:int, deadline:int):
        self.id = package_id
        self.weight = weight
        self.profit = profit
        self.deadline = deadline

    def calculate_penalty(self):
        """Beräknar straffavgiften om deadline är passerad."""
        if self.deadline < 0:
            return -(self.deadline ** 2)
        return 0
    
    def __repr__(self):
        return f'Package({self.id}, {self.weight}, {self.profit}, {self.deadline})'