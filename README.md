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

**Przykład wykorzystania w kodzie:**
```python
model = BottomUpGreedyDiscretizer()
model.read_data(data_path)
```
Fragment pochodzi z pliku `main.py`, linia 9.

- **`fit()`**
  - Główna metoda algorytmu.
  - Iteracyjnie wybiera cięcia, które maksymalizują liczbę odseparowanych par pomiędzy różnymi klasami.
  - Wynikowe cięcia są zapisywane w `selected_cuts`.

**Przykład wykorzystania w kodzie:**
```python
model.fit()
```
Fragment pochodzi z pliku `main.py`, linia 10.

- **`save_transformed(filepath)`**
  - Zapisuje przekształcone dane do pliku w formacie CSV.

**Przykład wykorzystania w kodzie:**
```python
model.save_transformed(output_path)
```
Fragment pochodzi z pliku `main.py`, linia 17.

---

### ** Analiza Wyników Dyskretyzacji**

#### Pary Niedeterministyczne
Po przekształceniu danych można przeanalizować ich jakość, sprawdzając liczbę par niedeterministycznych (par przykładów z różnymi etykietami, które znajdują się w tych samych przedziałach).

**Kod analizy:**
```python
intervals = df_disc.iloc[:, :-1].values.tolist()
labels = df_disc.iloc[:, -1].values
count = 0
for i in range(len(labels)):
    for j in range(i + 1, len(labels)):
        if labels[i] != labels[j] and intervals[i] == intervals[j]:
            count += 1
print(f"Pary niedeterministyczne: {count}")
```

#### Liczba Cięć
Dodatkowo można obliczyć liczbę cięć dla każdego atrybutu, aby ocenić złożoność dyskretyzacji.

**Kod analizy:**
```python
num_cuts = 0
for j in range(df_disc.shape[1] - 1):
    num_cuts += len(set(df_disc.iloc[:, j])) - 1
print(f"Liczba cięć: {num_cuts}")
```

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

---

## Autorzy

- Krzysztof Majka
- Norbert Zdziarski
- Jakub Rembisz
- Marcin Wąsacz
