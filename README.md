# Projekt Dyskretyzacji Danych

## Opis Projektu

Ten projekt implementuje algorytmy dyskretyzacji danych w celu przekształcenia ciągłych wartości atrybutów na wartości dyskretne. Dyskretyzacja jest kluczowym procesem w analizie danych i eksploracji danych, szczególnie w kontekście klasyfikacji i grupowania.

Główne algorytmy zaimplementowane w projekcie to:
- **Bottom-Up Greedy Discretizer**: Algorytm greedy (zachłanny) oparty na podejściu od dołu do góry.
- **Supervised Bottom-Up Discretizer**: Algorytm nadzorowany, który uwzględnia klasy decyzyjne przy budowie przedziałów.

## Struktura Projektu

- `Algorithm.py`: Zawiera implementację klasy `BottomUpGreedyDiscretizer`, która realizuje proces dyskretyzacji przy użyciu podejścia greedy.
- `BottomUpDiscretizer.py`: Zawiera implementację klasy `SupervisedBottomUpDiscretizer`, bazującej na modelu nadzorowanym.
- `main.py`: Główny skrypt uruchamiający proces dyskretyzacji na danych wejściowych.
- Pliki danych (`data1.csv`, `data2.csv`, `data3.csv`): Przykładowe zestawy danych zawierające wartości ciągłe i klasy decyzyjne.

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

## Opis Algorytmów

### Bottom-Up Greedy Discretizer
- **Opis**: Algorytm greedy iteracyjnie dodaje cięcia w taki sposób, aby maksymalizować liczbę odseparowanych par przykładów z różnych klas.
- **Kluczowe Metody**:
  - `fit`: Przeprowadza proces wyszukiwania optymalnych cięć.
  - `transform`: Przekształca dane wejściowe na wartości dyskretne.
  - `save_transformed`: Zapisuje przekształcone dane do pliku.

### Supervised Bottom-Up Discretizer
- **Opis**: Algorytm nadzorowany grupuje wartości atrybutów w przedziały, uwzględniając separację klas decyzyjnych.
- **Kluczowe Metody**:
  - `fit`: Buduje przedziały na podstawie danych treningowych.
  - `transform`: Przekształca dane na podstawie wygenerowanych przedziałów.

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

## Uwagi

- Projekt zakłada, że dane wejściowe są w formacie CSV, gdzie kolumny `x1`, `x2` reprezentują atrybuty, a kolumna `Decyzja` to etykiety klas.
- Dyskretyzacja odbywa się niezależnie dla każdego pliku danych.
