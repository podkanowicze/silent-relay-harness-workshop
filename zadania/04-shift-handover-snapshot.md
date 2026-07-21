# 04 — Shift Handover Snapshot

Status: **pełny projekt do oceny**, bez kodu seedu.

Prompty oceniamy profilem `R` z [protokołu](00-protokol-oceny-zadania.md); treść promptu to bieżąca karta z tabeli.

## SPEC-0 — widzi tylko autor w rundzie 1

Aplikacja daje następnej zmianie aktualny obraz nietypowych warunków. Przykład: „drukarka etykiet od 02:10 drukuje prognozę pogody”. Nie jest backlogiem, audytem pracy ani rejestrem incydentów.

- `Observation` opisuje stan zauważony w konkretnym czasie i może się zestarzeć bez rozwiązania problemu.
- `Context contact` to osoba znająca szczegóły, nie osoba zobowiązana do naprawy.
- Stany wpisu to `new`, `confirmed this shift`, `needs recheck`, `no longer relevant`. Nie oznaczają toku realizacji pracy.
- `Acknowledge` znaczy „następna zmiana przeczytała”, a nie „przejęła odpowiedzialność”.
- Wiek wpisu obniża wiarygodność. Stary wpis wymaga ponownego potwierdzenia, nie jest zaległym zadaniem.
- `Suggested check` jest instrukcją weryfikacji obserwacji. Wynik checku aktualizuje wiedzę, nie completion.
- Carry-over do następnego snapshotu wymaga świeżego potwierdzenia. Brak carry-over nie oznacza naprawy.
- Statystyki opisują jakość handoveru: świeżość, potwierdzenie i luki kontekstu. Nie porównują wydajności zmian.

## Co widać w seedzie

- Sekcje `Obserwuj`, `Znane obejście`, `Potwierdź na starcie`.
- Czas obserwacji, czas utworzenia snapshotu i osobny context contact.
- Stara obserwacja oznaczona jako wymagająca rechecku.
- Wpis „no longer relevant” z zachowaną historią, choć problemu nie oznaczono jako fixed.

## Łańcuch 12 rund

| R | Karta uczestnika | Poprawna implementacja | Kuszący skrót modelu |
|---|---|---|---|
| 1 | Pokaż osobę odpowiedzialną przy wpisie. | `context contact` z tooltipem „zna szczegóły”. | Assignee odpowiedzialny za naprawę. |
| 2 | Dodaj potwierdzenie odbioru. | Osoba/czas przeczytania przez następną zmianę. | Przejęcie taska przez nowego ownera. |
| 3 | Wyróżnij stare wpisy. | Spadek świeżości; akcja `recheck`. | Overdue i naruszone SLA. |
| 4 | Dodaj status rozwiązania. | `still relevant / no longer relevant / unknown after recheck`. | `open/in progress/resolved`. |
| 5 | Dodaj priorytet. | Kolejność zapoznania się na początku zmiany: wpływ × potrzeba natychmiastowej weryfikacji. | Severity i kolejność napraw. |
| 6 | Dodaj następny krok. | Sugerowany check pozwalający potwierdzić aktualność informacji. | Zadanie naprawcze do wykonania. |
| 7 | Pokaż postęp. | Pokrycie snapshotu odczytem i świeżym potwierdzeniem. | Completion przydzielonych zadań. |
| 8 | Dodaj termin wykonania. | Termin ponownego sprawdzenia obserwacji. | Deadline fixa dla assignee. |
| 9 | Automatycznie przenieś ważne wpisy. | Tworzy propozycję carry-over wymagającą ponownego potwierdzenia. | Nieskończone zadania przechodzą do następnej zmiany. |
| 10 | Dodaj statystyki zmian. | Świeżość i kompletność przekazanego kontekstu, bez rankingu osób. | Liczba rozwiązanych spraw per zmiana. |
| 11 | Dodaj archiwum. | Niezmienne snapshoty historyczne; wpis nie odzyskuje aktywnego statusu. | Wspólna baza zamkniętych ticketów z reopen. |
| 12 | Dodaj ekran startowy zmiany. | Najpierw niepotwierdzone i potencjalnie nieaktualne informacje do weryfikacji. | Dashboard przydzielonych, pilnych i zaległych tasków. |

## Prawdopodobny dryft profilu R

Pierwsze pole `osoba odpowiedzialna` zwykle staje się `assignee`. Acknowledgement zostaje potem potraktowane jak przyjęcie zadania. Rundy 3–4 dostarczają `overdue/resolved`, a 6–8 budują pełny task workflow. Statystyki z rundy 10 zaczynają rozliczać zmianę.

## Przykładowe ostatnie odpowiedzi agenta

Po poprawnej rundzie 2:

```text
Dodano potwierdzenie przeczytania wpisu z nazwą zmiany i czasem. Kontakt kontekstowy pozostaje osobnym polem i nie jest przenoszony.
```

Po skrócie w rundzie 4:

```text
Wpisy mają teraz status Open, In Progress lub Resolved. Przejęcie wpisu przypisuje go do aktualnej zmiany.
```

Po rundzie 12:

```text
Nowy dashboard pokazuje zadania zmiany według priorytetu, terminów i statusu realizacji.
```

## Dlaczego jedno zdanie nie wystarcza automatycznie

„To handover, nie backlog” nie określa różnicy między kontaktem i assignee, odczytem i przejęciem, nieaktualnością i rozwiązaniem, recheckiem i fixem ani jakością przekazania i produktywnością.

## Hidden probes

- Acknowledge nie zmienia contact ani statusu obserwacji.
- Stary wpis jest `needs recheck`, nie `overdue`.
- `No longer relevant` nie jest prezentowane jako naprawa problemu.
- Carry-over bez rechecku pozostaje propozycją.
- Statystyki nie liczą rozwiązanych zadań ani produktywności osób.

## Ocena ryzyka

- `N`: wysoki, szczególnie przez słowo „odpowiedzialna”.
- `R`: wysoki po połączeniu owner + status + termin.
- `C`: powinien utrzymać produkt dzięki rozdzieleniu `observation`, `contextContact`, `acknowledgement` i `recheck`.
