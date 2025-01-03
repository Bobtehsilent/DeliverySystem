import pandas as pd
from src.objects.package import Package
from src.seeds import generate_lagerstatus, save_to_csv

output_file = 'data/lagerstatus.csv'

def load_data(file_path):
    """Läs in lagerstatus.csv och returnera en lista av Package objekt"""
    try:
        df = pd.read_csv(file_path)
        packages = [Package(row['paket_id'], row['vikt'], row['fortjanst'], row['deadline']) for index, row in df.iterrows()]
        return packages
    except FileNotFoundError:
        print(f'File not found: {file_path}')
        print('Seeding data...')
        data = generate_lagerstatus()
        save_to_csv(data, output_file)
        df = pd.read_csv(file_path)
        packages = [Package(row['paket_id'], row['vikt'], row['fortjanst'], row['deadline']) for index, row in df.iterrows()]
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