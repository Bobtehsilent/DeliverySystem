

from src.data_processing import load_data
from src.objects.package import Package
from pprint import pprint

df = load_data('data/lagerstatus.csv')

packages = [Package(row['paket_id'], row['vikt'], row['fortjanst'], row['deadline']) for index, row in df.iterrows()]

pprint(packages)