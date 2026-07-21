# Agenda — 90 minut

| Czas | Element |
|---:|---|
| 00–04 | Wyzwanie: 12 zmian, jedna cudza aplikacja |
| 04–08 | Neutralne demo runnera i rotacji |
| 08–12 | Zasady, przydziały, test narzędzi |
| 12–19 | Runda 1: pełny `SPEC-0` + `DELTA-1` |
| 19–59 | Rundy 2–11: tylko bieżąca delta, `10 × 4 min` |
| 59–65 | Runda 12: ostatnia zmiana + freeze |
| 65–68 | Każdy zgaduje: „do czego służy ta aplikacja?” |
| 68–75 | Odsłonięcie `SPEC-0` i checker |
| 75–85 | Debrief |
| 85–87 | Wnioski |
| 87–90 | Bufor |

Bilans: wprowadzenie `12 min`, praca `53 min`, odgadnięcie i wynik `10 min`, refleksja `12 min`, bufor `3 min`.

Kontrola: `12 + 53 + 10 + 12 + 3 = 90`.

## Runda 2–11

- `0:00–0:35` — przeczytanie delty, ostatniej odpowiedzi agenta i stanu aplikacji.
- `0:35–3:25` — dowolna liczba promptów w jednej sesji; timer jest informacyjny i nie resetuje się.
- `3:25–3:50` — blokada wejścia, draining.
- `3:50–4:00` — abort, scope gate, publikacja albo rollback, rotacja.

Po maks. 90 sekundach problemu z lokalnym Copilot CLI: lokalny adapter DeepAgents albo `TIMEOUT`.

Checker uruchamia wszystkie stacje równolegle; bez ręcznego testowania.

## Runda 12

- `0:00–4:45` — implementacja delty 12.
- `4:45–5:15` — draining.
- `5:15–6:00` — abort, freeze, snapshot.
