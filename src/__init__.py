from src.data_processing import load_data, validate_data
from src.objects.optimizer import Optimizer

def main():
    packages = load_data("data/lagerstatus.csv")
    
    valid, message = validate_data(packages)

    if not valid:
        print(message)

    optimizer = Optimizer(packages, num_trucks=10, max_capacity=800)

    optimizer.distribute_packages()

    optimizer.display_results()
    print("Sammanställning:", optimizer.get_summary())

if __name__ == "__main__":
    main()
