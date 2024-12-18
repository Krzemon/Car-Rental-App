# Car Rental App

## Author
- Przemysław Ryś

## Description
Aplikacja wypożyczalni samochodowej: 
- System autoryzacji umożliwia różne widoki aplikacji w zależności od użytkownika

---

## Różne poziomy dostępu

### Administrator
  - Zarządzanie flotą samochodową (dodawanie, edycja, usuwanie samochodów).
  - Zarządzanie użytkownikami systemu (pracownicy, klienci).
  - Dostęp do wszystkich raportów.

### Pracownik
  - Obsługa wypożyczeń i zwrotów samochodów.
  - Podgląd dostępnych samochodów i klientów.
  - Dostęp do wybranych raportów (np. stan floty).

### Klient
  - Przeglądanie dostępnych samochodów.
  - Składanie rezerwacji.
  - Podgląd i edycja własnych danych.

## Widoki aplikacji

### Logowanie:
  - Umożliwia logowanie w zależności od roli.
### Główne okno administratora:
  - Panel zarządzania flotą (formularze do edycji danych samochodów).
  - Panel zarządzania użytkownikami.
  - Panel raportów (przychody, najczęściej wypożyczane auta itp.).
### Główne okno pracownika:
  - Obsługa wypożyczeń (dodawanie nowych wypożyczeń).
  - Lista aktualnych wypożyczeń.
  - Raport stanu floty.
### Główne okno klienta:
  - Przeglądanie samochodów (filtrowanie, wyszukiwanie).
  - Historia rezerwacji.
  - Rezerwowanie samochodu.






### Week now (09.12 - 15.12)

- Implementation of more complex scenarios (may be moved to later weeks):
  1. Investment portfolio optimization
  2. Modeling the structure of fullerenes
  3. More to come if time allows
- Additional interface elements:
  - Progress indicators
  - Estimated time remaining

### Week 4 (16.12 - 22.12)

- Session save and restore 
- Importing user-defined scenarios
 
### Week 5 (06.01 - 12.01)

- Multi-run option (compare results across multiple runs for different set of parameters)

### Week 6 (13.01 - 19.01)

- Results exporting (plots, tables, etc.) in different formats

### Week 7 (20.01 - 24.01)

- final touches

***

## Description of project scenarios

#### 1. Investment portfolio optimization
Optimizing an investment portfolio involves finding the best distribution of investments, i.e. how much percentage to invest in a given asset (Maximize return while minimizing risk).

    - Objective function definition - Sharpe ratio maximization:
        |Sharpe = (E[R_p] - R_f) / \sigma_p            |
        |where:                                        |
        |E[R_p] - expected return of the portfolio     |
        |R_f - The risk-free rate (can be 0)           |
        |sigma_p - Portfolio risk (standard deviation) |
    - Import of historical data of specific assets
    - Pre-generation of random portfolios.
    - Portfolio evaluation based on the objective function.
    - Making “moves” in the space of possible portfolios to get closer to the optimal solution
    - Input data (List of assets, Expected returns and risks for each asset, Budget)
    - Limits (The sum of all allocations must be 100%)
    - The maximum share of any one asset may not exceed 
