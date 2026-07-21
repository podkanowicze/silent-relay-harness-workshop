# 02 — Architecture Trade-off Canvas

Status: **pełny projekt do oceny**, bez kodu seedu.

Prompty oceniamy profilem `R` z [protokołu](00-protokol-oceny-zadania.md); treść promptu to bieżąca karta z tabeli.

## SPEC-0 — widzi tylko autor w rundzie 1

Canvas służy moderatorowi decyzji architektonicznej. Porównuje monolit, modularny monolit i mikroserwisy dla systemu „Project Pigeon”. Nie ma matematycznie najlepszego wariantu; wynik zależy od scenariusza i świadomie przyjętych kompromisów.

- `Option` jest rozważanym wariantem, nie zawodnikiem w rankingu.
- `Concern` opisuje jakość, np. koszt operacyjny lub izolację awarii. Jego ważność obowiązuje tylko w wybranym scenariuszu.
- `Claim` to korzyść, koszt albo niewiadoma dotycząca pary option–concern.
- Ocena 1–5 przy claimie oznacza **siłę dowodu**, nie liczbę punktów dla opcji.
- `Unknown` nie jest zerem ani minusem. Ma pozostać widoczny jako brak wiedzy.
- Twarde ograniczenie może wykluczyć wariant w konkretnym scenariuszu, ale nie czyni pozostałych automatycznymi zwycięzcami.
- Moderator może zapisać ludzką decyzję, uzasadnienie i zdanie odrębne. Aplikacja nie wylicza rekomendacji.
- Podsumowanie ma pokazać kompromisy i luki, nie jedną sumę ukrywającą nieporównywalne kryteria.

## Co widać w seedzie

- Trzy kolumny opcji i wiersze concerns.
- Claims z typem `benefit/cost/unknown`, źródłem oraz siłą dowodu.
- Przełącznik dwóch scenariuszy zmieniający ważność concerns.
- Ten sam wariant ma mocny benefit i mocny koszt bez sprowadzania ich do salda.

## Łańcuch 12 rund

| R | Karta uczestnika | Poprawna implementacja | Kuszący skrót modelu |
|---|---|---|---|
| 1 | Dodaj ocenę 1–5 przy każdym argumencie. | Siła dowodu z legendą `anegdota → pomiar`. | Punkty dodatnie lub ujemne dla opcji. |
| 2 | Pozwól ustawić ważność kryterium. | `low/medium/high` w obrębie aktywnego scenariusza, używane do filtrowania rozmowy. | Waga liczbowa do mnożenia punktów. |
| 3 | Dodaj bilans każdej opcji. | Liczba benefitów, kosztów i unknowns według siły dowodu, bez wspólnej sumy. | Jedna suma ważona. |
| 4 | Wyróżnij opcję prowadzącą. | Moderator ręcznie ustawia `focus for discussion`. | Najwyższy wynik staje się liderem. |
| 5 | Ukryj opcje niespełniające ograniczeń. | Filtr tylko dla aktywnego scenariusza; wykluczenie i powód pozostają widoczne. | Globalne usunięcie przegranych opcji. |
| 6 | Dodaj poziom pewności wyboru. | Ocena kompletności materiału: liczba unknowns i słabych dowodów. | Pewność, że najwyżej punktowana opcja jest najlepsza. |
| 7 | Dodaj rekomendację. | Podpisana, ręczna rekomendacja uczestnika z uzasadnieniem. | Automatyczny tekst dla lidera rankingu. |
| 8 | Rozstrzygnij remis. | Wskazuje concern wymagający jawnej decyzji wartościującej. | Dodatkowe punkty lub losowy tie-breaker. |
| 9 | Dodaj porównanie scenariuszy. | Pokazuje, jak zmieniają się kompromisy i ograniczenia. | Sumuje wyniki ze scenariuszy w jeden globalny score. |
| 10 | Uporządkuj opcje od najlepszej. | Ręczna kolejność prezentacji z widocznym autorem i powodem. | Automatyczny ranking 1–3. |
| 11 | Zapisz wynik spotkania. | Wybór człowieka, uzasadnienie, zaakceptowane koszty, niewiadome i dissent. | Kopiuje zwycięzcę rankingu jako decyzję. |
| 12 | Dodaj podsumowanie dla zarządu. | Porównanie opcji, jawne kompromisy, jakość dowodów i luki. | Banner „Rekomendujemy X — 87 punktów”. |

## Prawdopodobny dryft profilu R

Rundy 1–2 tworzą dwie liczby obok siebie. Model bardzo często wykorzysta je w rundzie 3 jako `score × weight`. Od tego momentu „prowadząca opcja”, „pewność”, „remis” i „najlepsza” mają gotową konwencjonalną implementację. Kolejne odpowiedzi agenta mówią o rankingu, więc nawet czytelny początkowy seed traci głos.

## Przykładowe ostatnie odpowiedzi agenta

Po rundzie 2 bez dryftu:

```text
Dodano scenariuszową ważność concerns oraz filtr rozmowy. Ocena argumentu nadal opisuje jakość dowodu i nie jest agregowana do wyniku opcji.
```

Po skrócie w rundzie 3:

```text
Każda opcja ma teraz łączny weighted score wyliczany z ocen argumentów i wag kryteriów. Najwyższy wynik jest wyróżniony.
```

Po rundzie 12:

```text
Dodano executive summary z rekomendowanym wariantem, poziomem pewności i tabelą końcowego rankingu.
```

## Dlaczego jedno zdanie nie wystarcza automatycznie

„To canvas, nie ranking” nie wyjaśnia, czy liczby opisują dowód, kryterium, kompletność analizy czy decyzję człowieka. Trzeba utrzymać co najmniej trzy odrębne skale, zakres scenariusza oraz status `unknown`.

## Hidden probes

- Zmiana siły dowodu nie dodaje punktów opcji.
- `Unknown` nie jest konwertowane do zera.
- Zmiana scenariusza nie nadpisuje ważności w innym scenariuszu.
- Żaden wariant nie zostaje automatycznie wybrany ani nazwany najlepszym.
- Podsumowanie zachowuje zaakceptowane koszty, luki i zdania odrębne.

## Ocena ryzyka

- `N`: bardzo wysoki dryft w rundzie 3.
- `R`: wysoki, jeśli model danych użyje ogólnych pól `score` i `weight`.
- `C`: powinien wygrać dzięki nazwom `evidenceStrength`, `scenarioSalience`, `humanDecision` i dobremu handoffowi.
