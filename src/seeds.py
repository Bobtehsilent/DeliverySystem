import random
import csv
from src.objects.package import Package

output_file = 'data/lagerstatus.csv'

def generate_lagerstatus(num_paket:int=500):
    packages = []
    for _ in range(num_paket):
        paket_id = random.randint(1_000_000, 9_999_999)
        vikt = round(random.uniform(0.1, 20), 2)
        förtjänst = random.randint(1, 10)
        deadline = random.randint(-5, 10)
        package = Package(paket_id, vikt, förtjänst, deadline)
        packages.append(package)

    return packages

def save_to_csv(packages, file_name):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['paket_id', 'vikt', 'fortjanst', 'deadline'])
        for package in packages:
            writer.writerow([package.id, package.weight, package.profit, package.deadline])

if __name__ == '__main__':
    data = generate_lagerstatus()
    save_to_csv(data, output_file)
    print(f'Generated {len(data)} rows and saved to {output_file}')