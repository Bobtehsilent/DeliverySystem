import pandas as pd
import os
from src.objects.package import Package
from src.seeds import seed_packages

output_file = 'data/lagerstatus.csv'

def load_data(file_path):
    """Läs in lagerstatus.csv och returnera en lista av Package objekt"""
    try:
        df = pd.read_csv(file_path)
        packages = [Package(row['Paket_id'], row['Vikt'], row['Förtjänst'], row['Deadline']) for index, row in df.iterrows()]
        return packages
    except FileNotFoundError:
        print(f'File not found: {file_path}')
        print('Seeding data...')
        seed_packages(n_iter=100, target_path=output_file)
        df = pd.read_csv(file_path)
        packages = [Package(row['Paket_id'], row['Vikt'], row['Förtjänst'], row['Deadline']) for index, row in df.iterrows()]
        return packages

def validate_data(packages):
    """Validera datan: kontrollera värden"""
    if packages is None or len(packages) == 0:
        return False, "Package list is empty"
    if any(package.weight <= 0 for package in packages):
        return False, "Weight must be greater than 0"
    return True, "Validation done"

def save_results(optimizer, result_dir, timestamp):
    """
    Save optimization results and truck details to files.
    
    Args:
        optimizer (Optimizer): The optimizer instance containing the results.
        result_dir (str): The directory to save the results.
        timestamp (str): Timestamp for naming the result files.
    """
    os.makedirs(result_dir, exist_ok=True)

    # Save optimization results
    result_file = os.path.join(result_dir, f"{timestamp}_results.txt")
    with open(result_file, "w", encoding="utf-8") as file:
        total_profit = sum(truck.get_total_profit() for truck in optimizer.trucks)
        total_penalty = sum(
            p.calculate_penalty() for truck in optimizer.trucks for p in truck.packages
        )
        file.write("\n--- Resultat för Optimering ---\n")
        for truck in optimizer.trucks:
            file.write(str(truck) + "\n")
        file.write(f"\nTotalt antal paket kvar i lager: {len(optimizer.packages) - sum(len(truck.packages) for truck in optimizer.trucks)}\n")
        file.write(f"Total Förtjänst (levererade paket): {total_profit}\n")
        file.write(f"Totala Straffavgifter: {total_penalty}\n")
        file.write(f"Actual total profit: {total_profit + total_penalty}\n")

    # Save truck details
    truck_details_file = os.path.join(result_dir, f"{timestamp}_truck_details.txt")
    optimizer.export_truck_details(truck_details_file)

    print(f"Results saved: {result_file}")
    print(f"Truck details saved: {truck_details_file}")

    return result_file, truck_details_file

if __name__ == '__main__':
    packages = load_data('data/lagerstatus.csv')
    valid, message = validate_data(packages)
    print(message)