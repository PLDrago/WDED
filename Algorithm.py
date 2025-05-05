import pandas as pd
import numpy as np
import csv
from collections import Counter
from itertools import combinations
import os
import time

class BottomUpGreedyDiscretizer:
    def __init__(self):
        self.cuts = {}            # Wszystkie możliwe cięcia (dla każdego atrybutu)
        self.selected_cuts = {}   # Wybrane cięcia po dyskretyzacji (dla każdego atrybutu)

    def read_data(self, filepath):
        """Wczytuje dane z pliku CSV"""
        df = pd.read_csv(filepath)
        self.X = df.iloc[:, :-1].values  # cechy
        self.y = df.iloc[:, -1].values   # decyzje
        return df

    def generate_all_possible_cuts(self):
        """Generuje możliwe cięcia między punktami o różnych klasach"""
        for attr in range(self.X.shape[1]):
            self.cuts[attr] = []
            vals_labels = sorted(zip(self.X[:, attr], self.y))
            cuts = set()
            for i in range(len(vals_labels) - 1):
                v1, y1 = vals_labels[i]
                v2, y2 = vals_labels[i + 1]
                if y1 != y2 and v1 != v2:
                    cut = (v1 + v2) / 2
                    cuts.add(cut)
            self.cuts[attr] = sorted(cuts)

    def get_partition_keys(self, X, selected_cuts):
        """Zwraca klucze przedziałowe dla każdego obiektu"""
        result = []
        for row in X:
            key = []
            for attr in range(self.X.shape[1]):
                cuts = selected_cuts[attr]
                val = row[attr]
                for i, cut in enumerate(cuts):
                    if val <= cut:
                        key.append(i)
                        break
                else:
                    key.append(len(cuts))
            result.append(tuple(key))
        return result

    def count_separated_pairs(self, keys):
        """Zlicza liczbę par obiektów o różnych klasach w różnych przedziałach"""
        count = 0
        for i, j in combinations(range(len(keys)), 2):
            if keys[i] != keys[j] and self.y[i] != self.y[j]:
                count += 1
        return count

    def fit(self):
        """Główna funkcja: wybór najlepszych cięć metodą zachłanną"""
        self.generate_all_possible_cuts()
        current_cuts = {i: [] for i in range(self.X.shape[1])}
        current_keys = self.get_partition_keys(self.X, current_cuts)
        current_score = self.count_separated_pairs(current_keys)

        all_candidates = [(attr, cut) for attr in range(self.X.shape[1]) for cut in self.cuts[attr]]
        used = set()

        while True:
            best_gain = 0
            best_candidate = None

            for attr, cut in all_candidates:
                if (attr, cut) in used:
                    continue
                temp_cuts = {k: list(v) for k, v in current_cuts.items()}
                temp_cuts[attr].append(cut)
                temp_cuts[attr].sort()
                keys = self.get_partition_keys(self.X, temp_cuts)
                score = self.count_separated_pairs(keys)
                gain = score - current_score
                if gain > best_gain:
                    best_gain = gain
                    best_candidate = (attr, cut)

            if best_candidate is None:
                break

            attr, cut = best_candidate
            current_cuts[attr].append(cut)
            current_cuts[attr].sort()
            current_score += best_gain
            used.add((attr, cut))
            print(f"Dodano cięcie: x{attr+1} = {cut:.3f}, suma odseparowanych par: {current_score}")

        self.selected_cuts = current_cuts

    def weighted_purity(self, selected_cuts):
        """Dodatkowe kryterium jakości – średnia ważona dominacja klasy w przedziałach"""
        keys = self.get_partition_keys(self.X, selected_cuts)
        group_map = {}

        for key, label in zip(keys, self.y):
            group_map.setdefault(key, []).append(label)

        total = len(self.y)
        dominant_sum = sum(Counter(group).most_common(1)[0][1] for group in group_map.values())

        return dominant_sum / total if total > 0 else 0

    def transform(self):
        """Zamienia wartości numeryczne na przedziały tekstowe"""
        result = []
        for row in self.X:
            new_row = []
            for attr in range(self.X.shape[1]):
                cuts = self.selected_cuts[attr]
                val = row[attr]
                for i, cut in enumerate(cuts):
                    if val <= cut:
                        interval = f"({cuts[i-1] if i > 0 else '-inf'}; {cut}]"
                        break
                else:
                    interval = f"({cuts[-1] if cuts else '-inf'}; inf)"
                new_row.append(interval)
            result.append(new_row)
        return result

    def save_transformed(self, filepath):
        """Zapisuje dane z przedziałami do pliku"""
        rows = self.transform()
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)  # separator domyślny: przecinek
            for row, label in zip(rows, self.y):
                writer.writerow(row + [label])

    def test(self, disc_path, orig_path):
        """Moduł testujący zgodność z oryginałem"""
        df_disc = pd.read_csv(disc_path, sep=',', header=None)
        df_orig = pd.read_csv(orig_path)

        # 1. Sprawdzenie liczby wierszy
        assert df_disc.shape[0] == df_orig.shape[0], "Liczba wierszy niezgodna"
        print("✅ Liczba wierszy zgodna")

        # 2. Sprawdzenie poprawności przynależności do przedziału
        for i in range(df_orig.shape[0]):
            for j in range(df_orig.shape[1] - 1):
                val = df_orig.iloc[i, j]
                interval = df_disc.iloc[i, j]
                parts = interval.strip('()[]').split(';')
                if len(parts) != 2:
                    raise ValueError(f"❌ Błędny przedział: {interval}")
                left, right = parts
                left = float(left) if left != '-inf' else float('-inf')
                right = float(right) if right != 'inf' else float('inf')
                assert left < val <= right, f"Obiekt {i}, kolumna {j}: {val} nie pasuje do {interval}"
        print("✅ Wszystkie wartości w przedziałach")

        # 3. Zliczenie par niedeterministycznych
        intervals = df_disc.iloc[:, :-1].values.tolist()
        labels = df_disc.iloc[:, -1].values
        count = 0
        for i in range(len(labels)):
            for j in range(i + 1, len(labels)):
                if labels[i] != labels[j] and intervals[i] == intervals[j]:
                    count += 1
        print(f"Pary niedeterministyczne: {count}")

        # 4. Liczba unikalnych cięć
        num_cuts = 0
        for j in range(df_disc.shape[1] - 1):
            num_cuts += len(set(df_disc.iloc[:, j])) - 1
        print(f"Liczba cięć: {num_cuts}")
