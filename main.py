import os
import time
from discretizer import BottomUpGreedyDiscretizer

def run_discretization(data_paths):
    for data_path in data_paths:
        print(f"\n⏳ Przetwarzanie pliku: {data_path}")
        model = BottomUpGreedyDiscretizer()
        model.read_data(data_path)
        model.fit()

        # Zapis wyniku
        output_path = os.path.join(
            os.path.dirname(data_path),
            "DISC" + os.path.basename(data_path)
        )
        model.save_transformed(output_path)
        print(f"✅ Zapisano: {output_path}")

if __name__ == "__main__":
    # Lista plików wejściowych
    data_files = ['data1.csv', 'data2.csv', 'data3.csv']

    # Uruchomienie z mierzeniem czasu
    start = time.time()
    run_discretization(data_files)
    end = time.time()

    print(f"\n⏱️ Czas dyskretyzacji wszystkich plików: {end - start:.2f} sekund")
