from collections import Counter
from itertools import combinations


class Interval:
    def __init__(self, values_classes):
        self.values_classes = values_classes  # [(value, class)]
        self.values_classes.sort()
        self.start = self.values_classes[0][0]
        self.end = self.values_classes[-1][0]

    def merge(self, other):
        return Interval(self.values_classes + other.values_classes)

    def __repr__(self):
        return f"[{self.start:.2f}, {self.end:.2f}]"


class SupervisedBottomUpDiscretizer:
    def __init__(self, max_bins=5):
        self.max_bins = max_bins
        self.intervals = []

    def _separation_score(self, intervals):
        """Zlicza liczbę granic między przedziałami, gdzie zmienia się klasa."""
        separated = 0
        for i in range(len(intervals) - 1):
            right_class = intervals[i].values_classes[-1][1]
            left_class = intervals[i + 1].values_classes[0][1]
            if right_class != left_class:
                separated += 1
        return separated

    def fit(self, values, labels):
        data = sorted(zip(values, labels), key=lambda x: x[0])
        intervals = [Interval([point]) for point in data]

        while len(intervals) > self.max_bins:
            best_loss = float('inf')
            best_index = -1

            for i in range(len(intervals) - 1):
                temp_intervals = (
                    intervals[:i]
                    + [intervals[i].merge(intervals[i + 1])]
                    + intervals[i + 2:]
                )
                current_sep = self._separation_score(intervals)
                new_sep = self._separation_score(temp_intervals)
                loss = current_sep - new_sep  # chcemy minimalizować utratę separowalności

                if loss < best_loss:
                    best_loss = loss
                    best_index = i

            merged = intervals[best_index].merge(intervals[best_index + 1])
            intervals = intervals[:best_index] + [merged] + intervals[best_index + 2:]

        self.intervals = intervals
        return self

    def transform(self, values):
        bins = []
        for v in values:
            for i, interval in enumerate(self.intervals):
                if interval.start <= v <= interval.end:
                    bins.append(i)
                    break
        return bins

    def fit_transform(self, values, labels):
        self.fit(values, labels)
        return self.transform(values)

    def get_bins(self):
        return [(iv.start, iv.end) for iv in self.intervals]

    def count_separated_pairs(self, values, labels):
        """Zlicza liczbę par obiektów skutecznie odseparowanych przez cięcia."""
        bins = self.transform(values)
        separated = 0
        n = len(values)
        for i in range(n):
            for j in range(i + 1, n):
                if labels[i] != labels[j] and bins[i] != bins[j]:
                    separated += 1
        return separated