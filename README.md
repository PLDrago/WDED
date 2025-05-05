# Projekt Dyskretyzacji Danych

## Opis Projektu

Ten projekt implementuje algorytmy dyskretyzacji danych, które przekształcają wartości ciągłe na wartości dyskretne. Dyskretyzacja jest kluczowym procesem w analizie danych, szczególnie w przygotowaniu danych do klasyfikacji i eksploracji. W projekcie zaimplementowano dwa algorytmy:
- **Bottom-Up Greedy Discretizer**: Algorytm zachłanny oparty na podejściu od dołu do góry.
- **Supervised Bottom-Up Discretizer**: Algorytm nadzorowany, który uwzględnia klasy decyzyjne przy budowie przedziałów.

## Struktura Projektu

- `Algorithm.py`: Implementacja klasy `BottomUpGreedyDiscretizer`.
- `BottomUpDiscretizer.py`: Implementacja klasy `SupervisedBottomUpDiscretizer`.
- `main.py`: Główny skrypt uruchamiający proces dyskretyzacji na danych wejściowych.
- Pliki danych (`data1.csv`, `data2.csv`, `data3.csv`): Przykładowe dane wejściowe.

---

## Opis Algorytmów i Kluczowych Metod

### **1. Bottom-Up Greedy Discretizer (`Algorithm.py`)**

#### Główne Metody
- **`read_data(filepath)`**
  - Wczytuje dane wejściowe z pliku CSV.
  - Dane są dzielone na macierz cech (`X`) i wektor etykiet (`y`).

- **`generate_all_possible_cuts()`**
  - Generuje wszystkie możliwe "cięcia" dla atrybutów.
  - Cięcie jest umieszczane w miejscu, gdzie wartości ciągłe zmieniają klasę decyzyjną.

- **`get_partition_keys(X, selected_cuts)`**
  - Dzieli dane na przedziały na podstawie wybranych cięć.
  - Każdy wiersz danych jest przypisywany do klucza odpowiadającego jego przedziałowi.

- **`count_separated_pairs(keys)`**
  - Oblicza liczbę par przykładów, które są odseparowane przez aktualne klucze oraz należą do różnych klas.

- **`fit()`**
  - Główna metoda algorytmu.
  - Iteracyjnie wybiera cięcia, które maksymalizują liczbę odseparowanych par pomiędzy różnymi klasami.
  - Wynikowe cięcia są zapisywane w `selected_cuts`.

- **`transform()`**
  - Przekształca dane wejściowe na wartości dyskretne, przypisując każdą wartość do odpowiedniego przedziału.

- **`save_transformed(filepath)`**
  - Zapisuje przekształcone dane do pliku w formacie CSV.

---

### **2. Supervised Bottom-Up Discretizer (`BottomUpDiscretizer.py`)**

#### Główne Metody
- **`fit(values, labels)`**
  - Tworzy początkowe przedziały dla każdej wartości ciągłej.
  - Iteracyjnie łączy sąsiednie przedziały, jeśli ich połączenie minimalizuje stratę separacji klas.

- **`_separation_score(intervals)`**
  - Oblicza liczbę odseparowanych klas w przedziałach.
  - Im wyższy wynik, tym lepsza separacja.

- **`merge(other)` (dla klasy `Interval`)**
  - Łączy dwa przedziały w jeden nowy przedział.

- **`transform(values)`**
  - Przekształca dane wejściowe na wartości dyskretne, przypisując każdą wartość do odpowiedniego przedziału.

- **`fit_transform(values, labels)`**
  - Przeprowadza zarówno proces budowy przedziałów, jak i dyskretyzacji danych.

- **`count_separated_pairs(values, labels)`**
  - Oblicza liczbę odseparowanych par danych w zależności od ich przynależności do różnych klas.

---

## Instrukcja Użycia

### Krok 1: Przygotowanie Środowiska
1. Upewnij się, że masz zainstalowane wymagane pakiety Python:
   ```bash
   pip install pandas numpy
   ```

2. Umieść pliki danych (`data1.csv`, `data2.csv`, `data3.csv`) w tym samym katalogu co skrypty Pythona.

### Krok 2: Uruchomienie Skryptu
Uruchom skrypt `main.py`, aby przeprowadzić dyskretyzację danych:
```bash
python main.py
```

### Krok 3: Wyniki
Wyniki dyskretyzacji zostaną zapisane w plikach z prefiksem `DISC` w nazwie, np. `DISCdata1.csv`. Każdy wynikowy plik zawiera zbinowane wartości atrybutów oraz klasy decyzyjne.

---

## Przykładowe Dane

### Plik `data1.csv`
```csv
x1,x2,Decyzja
1.0,5.0,1
2.5,6.7,2
...
```

### Wynik Dyskretyzacji dla `data1.csv`
```csv
x1_bin,x2_bin,Decyzja
(0.5; 1.7],(4.2; 5.5],1
...
```

---

## Uwagi

- Projekt zakłada, że dane wejściowe są w formacie CSV, gdzie kolumny `x1`, `x2` reprezentują atrybuty, a kolumna `Decyzja` to etykiety klas.
- Dyskretyzacja odbywa się niezależnie dla każdego pliku danych.
