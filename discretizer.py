import pandas as pd
import numpy as np
import csv
from collections import Counter
from itertools import combinations
import os

class BottomUpGreedyDiscretizer:
    def __init__(self):
        self.cuts = {0: [], 1: []}
        self.selected_cuts = {0: [], 1: []}

    def read_data(self, filepath):
        df = pd.read_csv(filepath)  # domyślny separator to przecinek
        self.X = df.iloc[:, :-1].values
        self.y = df.iloc[:, -1].values
        return df

    def generate_all_possible_cuts(self):
        for attr in [0, 1]:
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
        result = []
        for row in X:
            key = []
            for attr in [0, 1]:
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
        count = 0
        for i, j in combinations(range(len(keys)), 2):
            if keys[i] != keys[j] and self.y[i] != self.y[j]:
                count += 1
        return count

    def fit(self):
        self.generate_all_possible_cuts()
        current_cuts = {0: [], 1: []}
        current_keys = self.get_partition_keys(self.X, current_cuts)
        current_score = self.count_separated_pairs(current_keys)

        all_candidates = [(attr, cut) for attr in [0, 1] for cut in self.cuts[attr]]
        used = set()

        while True:
            best_gain = 0
            best_candidate = None

            for attr, cut in all_candidates:
                if (attr, cut) in used:
                    continue
                temp_cuts = current_cuts.copy()
                temp_cuts[attr] = sorted(current_cuts[attr] + [cut])
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
        keys = self.get_partition_keys(self.X, selected_cuts)
        group_map = {}

        for key, label in zip(keys, self.y):
            if key not in group_map:
                group_map[key] = []
            group_map[key].append(label)

        total = len(self.y)
        dominant_sum = 0
        for group in group_map.values():
            count = Counter(group)
            dominant = count.most_common(1)[0][1]
            dominant_sum += dominant

        return dominant_sum / total if total > 0 else 0

    def transform(self):
        result = []
        for row in self.X:
            new_row = []
            for attr in [0, 1]:
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
        rows = self.transform()
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            for row, label in zip(rows, self.y):
                writer.writerow(row + [label])
