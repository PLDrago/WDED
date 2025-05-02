import csv
from itertools import combinations
from collections import defaultdict

class GreedyDiscretizerFromIntervals:
    def __init__(self):
        self.selected_cuts = set()
        self.all_possible_cuts = set()
        self.cut_axis_map = defaultdict(set)  # np. {(0, '(1.8; 1.95]')}
        self.data = []
        self.labels = []

    def parse_csv(self, filepath):
        with open(filepath, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if len(row) != 3:
                    continue
                attr1, attr2, label = row
                self.data.append([attr1.strip(), attr2.strip()])
                self.labels.append(label.strip())
                self.all_possible_cuts.add((0, attr1.strip()))
                self.all_possible_cuts.add((1, attr2.strip()))
                self.cut_axis_map[0].add(attr1.strip())
                self.cut_axis_map[1].add(attr2.strip())

    def current_partition(self, active_cuts):
        """
        Zwraca etykietę przedziału dla każdego obiektu jako krotkę (dla każdego atrybutu).
        """
        partitions = []
        for obj in self.data:
            key = []
            for attr_index in [0, 1]:
                val = obj[attr_index]
                key.append(val if (attr_index, val) in active_cuts else 'ALL')
            partitions.append(tuple(key))
        return partitions

    def count_separated_pairs(self, partitions, labels):
        """
        Liczy liczbę par obiektów, które są w różnych przedziałach i mają różne etykiety.
        """
        separated = 0
        for (i, j) in combinations(range(len(partitions)), 2):
            if partitions[i] != partitions[j] and labels[i] != labels[j]:
                separated += 1
        return separated

    def fit(self):
        current_cuts = set()
        partitions = self.current_partition(current_cuts)
        max_separated = self.count_separated_pairs(partitions, self.labels)

        while True:
            best_cut = None
            best_gain = 0

            for cut in self.all_possible_cuts - current_cuts:
                temp_cuts = current_cuts | {cut}
                partitions = self.current_partition(temp_cuts)
                separated = self.count_separated_pairs(partitions, self.labels)
                gain = separated - max_separated

                if gain > best_gain:
                    best_gain = gain
                    best_cut = cut

            if best_cut is None:
                break  # brak przyrostu

            current_cuts.add(best_cut)
            max_separated += best_gain
            print(f"Dodano cięcie {best_cut}, suma odseparowanych par: {max_separated}")

        self.selected_cuts = current_cuts

    def transform(self):
        """
        Zwraca dane z etykietami przedziałów tylko tam, gdzie zastosowano cięcia.
        """
        transformed = []
        for obj in self.data:
            new_obj = []
            for attr_index in [0, 1]:
                val = obj[attr_index]
                new_obj.append(val if (attr_index, val) in self.selected_cuts else 'ALL')
            transformed.append(new_obj)
        return transformed

disc = GreedyDiscretizerFromIntervals()
disc.parse_csv("DISC_DATA.csv")
disc.fit()

print("\nWybrane cięcia:")
print(disc.selected_cuts)

print("\nZdyskretyzowane dane:")
for row in disc.transform():
    print(row)
