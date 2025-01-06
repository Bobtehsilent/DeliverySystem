import pandas as pd
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

if __name__ == '__main__':
    packages = load_data('data/lagerstatus.csv')
    valid, message = validate_data(packages)
    print(message)