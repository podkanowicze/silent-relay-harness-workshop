# Bank zadań — 12 pełnych łańcuchów do oceny

Każdy plik zawiera materiał do oceny rzeczywistego łańcucha: `SPEC-0`, seed logiczny, 12 kart, prawdopodobne skróty modelu i hidden probes. Kod seedów powstanie po akceptacji.

Założenia wspólne: [cel i mechanika banku](00-cel-i-zalozenia-do-akceptacji.md), [protokół oceny prompt → odpowiedź → dryft](00-protokol-oceny-zadania.md) oraz [porównawcza macierz prawdopodobieństwa dryftu](00-macierz-prawdopodobienstwa-dryftu.md).

## Aktualnie oceniany nowy kierunek

[FINAL-01 — Skrzydła z małych miast](FINAL-01-skrzydla-z-malych-miast.md) — kompletna instrukcja prowadzącego, `SPEC-0`, routing, 12 kart i końcowa ocena autora.

[Analiza projektowa tego ćwiczenia](PILOT-01-dofinansowane-loty-do-disneylandu.md) pozostaje materiałem roboczym.

| # | Zadanie | Główna oś dryftu |
|---|---|---|
| 01 | [Debugging Hypothesis Board](01-debugging-hypothesis-board.md) | hipoteza → ticket do naprawy |
| 02 | [Architecture Trade-off Canvas](02-architecture-tradeoff-canvas.md) | kompromisy → automatyczny ranking |
| 03 | [Meeting Parking Lot](03-meeting-parking-lot.md) | temat rozmowy → zadanie projektowe |
| 04 | [Shift Handover Snapshot](04-shift-handover-snapshot.md) | chwilowy kontekst → backlog i rozliczenie |
| 05 | [Premortem Postcards](05-premortem-postcards.md) | fikcyjny scenariusz → prognoza ryzyka |
| 06 | [Customer Quote Sorter](06-customer-quote-sorter.md) | materiał jakościowy → statystyka populacji |
| 07 | [Data Cleaning Preview](07-data-cleaning-preview.md) | propozycja na kopii → edycja źródła prawdy |
| 08 | [Policy Interpretation Cards](08-policy-interpretation-cards.md) | porównanie odczytań → werdykt zgodności |
| 09 | [Interview Evidence Board](09-interview-evidence-board.md) | kompletność dowodów → ocena człowieka |
| 10 | [Incident Causal Map](10-incident-causal-map.md) | mapa niepewności → ranking winnych |
| 11 | [Workshop Energy Weather](11-workshop-energy-weather.md) | anonimowa pogoda grupy → monitoring osób |
| 12 | [Runbook Rehearsal](12-runbook-rehearsal.md) | ćwiczenie i debrief → egzamin pracownika |

Każdy poprawny i błędny produkt jest w pełni realizowalny jako lokalna aplikacja vanilla HTML/CSS/JS. Żadne zadanie nie opiera dryftu na udawanej integracji, backendzie ani akcji na zewnętrznym systemie.

## Ocena przed budową seedów

Przy każdym zadaniu wybierz: `zostaje`, `zmienić łańcuch`, `wyrzucić`. Nie budujemy seedu, jeżeli dryft nie jest wiarygodny dla profilu rozsądnego developera.
