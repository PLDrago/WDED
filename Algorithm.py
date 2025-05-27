import pandas as pd
import numpy as np
import csv
from collections import defaultdict
from bisect import bisect_right

class BottomUpGreedyDiscretizer:
    def __init__(self):
        self.cuts = {}
        self.selected_cuts = {}

    def read_data(self, filepath):
        df = pd.read_csv(filepath, header=None)
        self.X = df.iloc[:, :-1].to_numpy()
        self.y = df.iloc[:, -1].to_numpy()
        n_attrs = self.X.shape[1]
        self.cuts = {i: [] for i in range(n_attrs)}
        self.selected_cuts = {i: [] for i in range(n_attrs)}
        return df

    def generate_all_possible_cuts(self):
        for attr in range(self.X.shape[1]):
            vals_labels = sorted(zip(self.X[:, attr], self.y))
            cuts = []
            last_cut = None
            for i in range(len(vals_labels) - 1):
                v1, y1 = vals_labels[i]
                v2, y2 = vals_labels[i + 1]
                if y1 != y2 and v1 != v2:
                    cut = round((v1 + v2) / 2, 6)
                    if cut != last_cut:
                        cuts.append(cut)
                        last_cut = cut
            self.cuts[attr] = cuts

    def count_newly_separated(self, selected_cuts, new_cut, attr):
        idx = bisect_right(selected_cuts[attr], new_cut)
        left_cut = selected_cuts[attr][idx - 1] if idx != 0 else float('-inf')
        right_cut = selected_cuts[attr][idx] if idx != len(selected_cuts[attr]) else float('+inf')

        comp_arr = self.X[:, attr]
        sel = (comp_arr > left_cut) & (comp_arr <= right_cut)
        X = self.X[sel]
        y = self.y[sel]
        
        bucket = defaultdict(lambda: defaultdict(lambda: np.zeros(2)))
        for row, label in zip(X, y):
            key = []
            for attr_i in range(X.shape[1]):
                if attr_i == attr:
                    continue

                val = row[attr_i]
                cuts = selected_cuts[attr_i]
                idx = bisect_right(cuts, val)
                key.append(idx)
            lr = 1 - int(row[attr] <= new_cut)
            bucket[tuple(key)][label][lr] += 1

        partitions = list(bucket.values())
        count = 0

        for i in range(len(partitions)):
            c1 = partitions[i]
            for k1 in c1:
                for k2 in c1:
                    if k1 != k2:
                        count += c1[k1][0] * c1[k2][1]

        return count

    def fit(self):
        self.generate_all_possible_cuts()
        current_cuts = {k: [] for k in self.cuts}
        current_score = 0

        all_candidates = [(attr, cut) for attr in self.cuts for cut in self.cuts[attr]]

        while True:
            best_gain = 0
            best_candidate = None

            for attr, cut in all_candidates:
                gain = self.count_newly_separated(current_cuts, cut, attr)

                if gain > best_gain:
                    best_gain = gain
                    best_candidate = (attr, cut)

            if best_candidate is None or best_gain == 0:
                break

            attr, cut = best_candidate
            current_cuts[attr].append(cut)
            current_cuts[attr].sort()
            current_score += best_gain
            all_candidates.remove(best_candidate)

            print(f"Dodano cięcie: x{attr+1} = {cut:.3f}, separacja: {current_score}")

        self.selected_cuts = current_cuts

    def transform(self):
        result = []
        for row in self.X:
            new_row = []
            for attr in range(self.X.shape[1]):
                val = row[attr]
                cuts = self.selected_cuts[attr]
                if not cuts:
                    new_row.append("(-inf; inf)")
                    continue

                for i, cut in enumerate(cuts):
                    left = cuts[i - 1] if i > 0 else '-inf'
                    if val <= cut:
                        new_row.append(f"({left}; {cut}]")
                        break
                else:
                    new_row.append(f"({cuts[-1]}; inf)")
            result.append(new_row)
        return result

    def save_transformed(self, filepath):
        rows = self.transform()
        with open(filepath, "w", newline='') as f:
            writer = csv.writer(f)
            for row, label in zip(rows, self.y):
                writer.writerow(row + [label])

class Algorithm:
    @staticmethod
    def example_algorithm(input_path):
        output_path = f"DISC{input_path}"
        disc = BottomUpGreedyDiscretizer()
        disc.read_data(input_path)
        disc.fit()
        disc.save_transformed(output_path)