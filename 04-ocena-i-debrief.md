# Ocena i debrief

## Wynik stacji

- Spełnione delty: `0–12`.
- Zachowane niezmienniki `SPEC-0`: `0–N`.
- Pierwsza runda utraty sensu.
- Końcowe zdanie autora kontra zdanie ostatniego uczestnika.
- `DRIFT`, regresje i `OVERSTEP`.
- Zmiany znaczenia terminów i tożsamości produktu.
- Błędy odziedziczone kontra wprowadzone w bieżącej rundzie.
- Sens `SPEC-0` czytelny w zachowaniu, strukturze i nazewnictwie kodu albo tylko w ostatniej odpowiedzi agenta.
- Zgodność promptu z deltą oraz sensem produktu.

Wynik diagnozuje przepływ kontekstu; nie służy do rankingu różnych zadań.

## Jakość ostatniej odpowiedzi agenta — `0–2` za element

1. Tożsamość produktu i cel bieżącej zmiany.
2. Aktualny stan.
3. Zachowane niezmienniki.
4. Niepewności bez wymyślania produktu od nowa.
5. Dowód: widoczny wynik lub zmieniony plik aplikacji.

## Debrief — 10 minut

| Czas | Pytanie |
|---:|---|
| 3 min | Kiedy aplikacja zaczęła znaczyć coś innego? |
| 3 min | Co autor wiedział, ale czego nie utrwalił? |
| 4 min | Jaki artefakt zatrzymałby zmianę tożsamości? |

## Wniosek

`tożsamość → niezmienniki → delta → stan → weryfikacja`

Działające zachowanie i czytelny kod są trwalszym kontekstem niż zapewnienie w odpowiedzi.
