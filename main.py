import time
from Algorithm import Algorithm

if __name__ == "__main__":
    data_files = ['ewal.csv']

    start = time.time()
    for file in data_files:
        Algorithm.example_algorithm(file)
    end = time.time()

    print(f"\nCzas dyskretyzacji wszystkich plików: {end - start:.3f} sekund")
