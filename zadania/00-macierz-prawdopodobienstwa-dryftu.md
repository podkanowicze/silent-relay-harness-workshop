# Macierz prawdopodobieństwa dryftu — ocena przed pilotem

To są hipotezy projektowe, nie wyniki pomiaru. Rzeczywiste odpowiedzi Copilota można ocenić dopiero na działających seedach.

| # | Dominujący wzorzec modelu | Pierwsza krytyczna karta | Mechanizm kaskady | Dryft profilu R |
|---|---|---|---|---|
| 01 | Jira / bug tracker | 2: właściciel | owner → closed → progress → overdue | średnio-wysoki |
| 02 | weighted decision matrix | 3: bilans | score + weight → winner → recommendation | wysoki |
| 03 | kanban zadań | 1: właściciel | assignee → deadline → done → backlog | średnio-wysoki |
| 04 | task/SLA tracker | 1: odpowiedzialna osoba | assignee → acknowledge → resolved → overdue | wysoki |
| 05 | risk register | 1–2: probability + impact | score → top risks → heatmap → mitigation | bardzo wysoki |
| 06 | customer analytics | 1–2: popularity + emotion | percent → average → trend → KPI | średnio-wysoki |
| 07 | spreadsheet editor | 1: popraw wartość | mutate source → delete duplicate → commit → clean export | wysoki bez technicznej ochrony seedu |
| 08 | compliance checker | 1: verdict | confidence → vote → active rule → mass classification | wysoki |
| 09 | hiring scorecard | 1: rating | skill score → overall → compare → rank | bardzo wysoki |
| 10 | blame/root-cause tree | 1–3: root + owner + percent | one cause → responsibility → ranking → verdict | wysoki |
| 11 | employee monitoring | 1: compare rounds | participant ID → personal trend → alerts → ranking | bardzo wysoki |
| 12 | quiz/exam | 1–2: result + points | correctness → score → leaderboard → certificate | bardzo wysoki |

## Co sprawdzić w pilocie

- Czy profil `R` naprawdę wybiera wskazany wzorzec, gdy widzi aktualny kod.
- Czy ostatnia odpowiedź agenta wzmacnia błędne znaczenie dla następnej osoby.
- Czy profil `C` potrafi zachować produkt bez znajomości przyszłych kart.
- Czy pierwsza krytyczna karta nie dryfuje zawsze — potrzebujemy wariancji między łańcuchami.
- Czy pojedyncza runda mieści się w timerze bez upraszczania testów.

## Najmocniejsze kandydaty do pierwszego pilota

1. `05 Premortem Postcards` — model ma bardzo mocny prior risk matrix.
2. `11 Workshop Energy Weather` — jedna niewinna decyzja o identyfikatorze zmienia wszystkie następne funkcje.
3. `12 Runbook Rehearsal` — oba produkty są kompletne w vanilla HTML, a różnica dotyczy użytkownika i celu.
4. `01 Debugging Hypothesis Board` — najbardziej zbliżone do realnej codziennej pracy developerów.
