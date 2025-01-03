from src.data_processing import load_data
from src.objects.optimizer import Optimizer

def main():
    packages = load_data("data/lagerstatus.csv")
    if not packages:
        print("Inga paket att optimera.")
        return

    optimizer = Optimizer(packages, max_trucks=20, max_capacity=800)
    optimizer.distribute_packages()
    optimizer.display_results()

if __name__ == "__main__":
    main()