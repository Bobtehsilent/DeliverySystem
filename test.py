

from src.data_processing import load_data
from src.objects.package import Package
from src.objects.truck import Truck
from src.objects.optimizer import Optimizer

# test_packages = [
#     Package(1, 300, 10, 2),   # Levereras i tid
#     Package(2, 500, 8, -1),  # Deadline missad med 1 dag
#     Package(3, 400, 6, -3),  # Deadline missad med 3 dagar
#     Package(4, 200, 4, 1),   # Levereras i tid
#     Package(5, 100, 2, 0),   # Deadline idag
# ]

# optimizer = Optimizer(test_packages, max_trucks=2, max_capacity=800)
# optimizer.distribute_packages()
# optimizer.display_results()
test_packages = [
    Package(1, 300, 10, 2),   # Levereras i tid
    Package(2, 500, 8, -1),  # Deadline missad med 1 dag
    Package(3, 400, 6, -3),  # Deadline missad med 3 dagar
]

# for p in test_packages:
#     print(p.effective_profit())

truck = Truck(1)
truck.add_package(Package(1, 300, 10, 2))  # Levereras i tid
truck.add_package(Package(2, 200, 8, -1))  # Deadline missad
truck.add_package(Package(3, 200, 6, -3))  # Deadline missad

for package in truck.packages:
    print(package)

print(truck.get_total_profit())

