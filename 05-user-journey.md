# User journey — jeden uczestnik

## Najważniejsze

`Uczestnik siedzi przy swoim komputerze. Jego licencja zostaje z nim; między rundami zmienia się pobrana stacja.`

Każda runda daje mu:

- kod aplikacji i ostatnią odpowiedź agenta,
- jedną kartę `DELTA-R`,
- puste pole promptu,
- świeżą lokalną sesję Copilota.

Tylko w rundzie 1 własnej stacji dostaje także kompletny `SPEC-0`. Nie dostaje wcześniejszych promptów, historii modelu ani przyszłych delt.

## Przykład: U1, 12 osób

| Runda | Stacja | Co widzi | Co robi |
|---:|---|---|---|
| 1 | `S1` | działający seed, pełny `SPEC-0`, `DELTA-1` | implementuje zmianę przy informacyjnym timerze |
| 2 | `S2` | kod, ostatnia odpowiedź, tylko `DELTA-2` | rekonstruuje produkt i prowadzi świeżą sesję |
| 3 | `S3` | kod, ostatnia odpowiedź, tylko `DELTA-3` | świeża sesja; jedna zmiana |
| 4–11 | `S4–S11` | kolejny kod, ostatnia odpowiedź i bieżąca delta | chroni albo nieświadomie przesuwa sens |
| 12 | `S12` | kod po 11 osobach, ostatnia odpowiedź, `DELTA-12` | implementuje finał i zgaduje tożsamość produktu |

Po rundzie 12 ukryty checker ocenia wszystkie repo.

## Rotacja

```text
R1:  U1→S1   U2→S2   U3→S3   ...   U12→S12
R2:  U1→S2   U2→S3   U3→S4   ...   U12→S1
...
R12: U1→S12  U2→S1   U3→S2   ...   U12→S11
```

## Ekran uczestnika

```text
LOKALNY RUNNER · STACJA 07 · RUNDA 6 · 03:42

DELTA-6
[krótka, niedookreślona potrzeba biznesowa]

OSTATNIA ODPOWIEDŹ AGENTA
[ostatnia finalna odpowiedź]

[pole: napisz prompt]
[WYŚLIJ — dostępne również po 00:00]
```

W rundzie 1 nad deltą pojawia się dodatkowy blok `SPEC-0`. Nie jest automatycznie kopiowany do modelu i znika po turze. Nie wolno zapisać go jako dokumentacji, długiego komentarza ani ukrytej treści aplikacji.

Przed pierwszym wysłaniem autor zapisuje w UI jedno zdanie „Ta aplikacja służy do…”. Controller pieczętuje je do końcowego revealu; nie trafia ono automatycznie do repo ani modelu.

Samo „zrób kolejną zmianę” daje agentowi wyłącznie możliwość zgadywania. Poprzednik nie znał następnej delty.

## Kliknięcia

1. Raz uruchamia runner i wpisuje kod parujący.
2. W każdej rundzie klika `Pobierz stację`.
3. Czyta deltę, kod i ostatnią odpowiedź agenta; w rundzie 1 także `SPEC-0`.
4. Prowadzi świeżą sesję dowolną liczbą promptów; timer nie resetuje się ani nie blokuje akcji.
5. Runner zachowuje tylko ostatnią odpowiedź agenta, bez limitu znaków, i wysyła propozycję; gate publikuje `PASS/DRIFT` albo odrzuca `OVERSTEP`.
6. Następna delta pojawia się dopiero w następnej rundzie.

Po rundzie 12 wpisuje jedno zdanie: „Ta aplikacja służy do…”. Dopiero potem prowadzący odsłania zdanie autora i pełny `SPEC-0`.

Bez cudzych tokenów, SSH do innych DevPodów i ręcznego wznawiania sesji.
