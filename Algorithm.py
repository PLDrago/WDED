import pandas as pd
import csv
from collections import defaultdict, Counter
from bisect import bisect_right

class BottomUpGreedyDiscretizer:
    def __init__(self):
        self.cuts = {}
        self.selected_cuts = {}

    def read_data(self, filepath):
        df = pd.read_csv(filepath)
        self.X = df.iloc[:, :-1].values
        self.y = df.iloc[:, -1].values
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

    def get_partition_keys(self, X, selected_cuts):
        result = []
        for row in X:
            key = []
            for attr in range(X.shape[1]):
                val = row[attr]
                cuts = selected_cuts[attr]
                idx = bisect_right(cuts, val)
                key.append(idx)
            result.append(tuple(key))
        return result

    def count_separated_pairs(self, keys):
        bucket = defaultdict(lambda: defaultdict(int))
        for key, label in zip(keys, self.y):
            bucket[key][label] += 1

        partitions = list(bucket.values())
        count = 0

        for i in range(len(partitions)):
            c1 = partitions[i]
            for j in range(i + 1, len(partitions)):
                c2 = partitions[j]
                for k1 in c1:
                    for k2 in c2:
                        if k1 != k2:
                            count += c1[k1] * c2[k2]
        return count

    def weighted_purity(self, selected_cuts):
        keys = self.get_partition_keys(self.X, selected_cuts)
        bucket = defaultdict(Counter)
        for key, label in zip(keys, self.y):
            bucket[key][label] += 1

        total = len(self.y)
        pure = sum(max(counter.values()) for counter in bucket.values())
        return pure / total if total else 0

    def fit(self):
        self.generate_all_possible_cuts()
        current_cuts = {k: [] for k in self.cuts}
        current_keys = self.get_partition_keys(self.X, current_cuts)
        current_score = self.count_separated_pairs(current_keys)

        all_candidates = [(attr, cut) for attr in self.cuts for cut in self.cuts[attr]]
        used = set()

        while True:
            best_gain = 0
            best_candidate = None

            for attr, cut in all_candidates:
                if (attr, cut) in used:
                    continue
                temp_cuts = {k: v.copy() for k, v in current_cuts.items()}
                temp_cuts[attr].append(cut)
                temp_cuts[attr].sort()

                temp_keys = self.get_partition_keys(self.X, temp_cuts)
                score = self.count_separated_pairs(temp_keys)
                gain = score - current_score

                if gain > best_gain:
                    best_gain = gain
                    best_candidate = (attr, cut)

            if best_candidate is None or best_gain == 0:
                break

            attr, cut = best_candidate
            current_cuts[attr].append(cut)
            current_cuts[attr].sort()
            current_score += best_gain
            used.add((attr, cut))

            purity = self.weighted_purity(current_cuts)
            print(f"Dodano cięcie: x{attr+1} = {cut:.3f}, separacja: {current_score}, czystość: {purity:.4f}")

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