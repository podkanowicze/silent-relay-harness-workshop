# 03 — Meeting Parking Lot

Status: **pełny projekt do oceny**, bez kodu seedu.

Prompty oceniamy profilem `R` z [protokołu](00-protokol-oceny-zadania.md); treść promptu to bieżąca karta z tabeli.

## SPEC-0 — widzi tylko autor w rundzie 1

Parking chroni agendę jednego spotkania. Moderator odkłada poboczny temat, wraca do niego w wolnym czasie i zapisuje rezultat rozmowy. Karta „kto nazwał serwer `final-final-2`?” nadal jest **tematem do omówienia**, nawet jeśli rozmowa stworzy osobne zadanie poza aplikacją.

- `Topic` należy do konkretnego `Meeting`, nie do produktu, sprintu ani zespołowego backlogu.
- Stany to `parked`, `discussing`, `discussed`. Oznaczają stan rozmowy, nie stan wykonania pracy.
- `Conversation lead` prowadzi rozmowę; nie jest assignee odpowiedzialnym za rezultat.
- `Return slot` to moment agendy, nie deadline.
- Priorytet oznacza wartość omówienia na tym spotkaniu względem pozostałego czasu.
- `Outcome` może być decyzją, pytaniem, linkiem do zewnętrznego action itemu albo `no decision`. Parking nie zarządza wykonaniem działań.
- Temat może być `discussed`, mimo że wynik brzmi „wrócimy za tydzień”.
- Po zakończeniu spotkania tablica jest snapshotem protokołu. Nie przenosi automatycznie tematów do kolejnego spotkania.

## Co widać w seedzie

- Kolumny `Parking`, `Teraz omawiamy`, `Omówione`.
- Timer spotkania i pozostały czas agendy.
- Karta omówiona bez decyzji oraz karta z linkiem tekstowym do działania poza aplikacją.
- Dane jednego nazwanego spotkania z datą i moderatorem.

## Łańcuch 12 rund

| R | Karta uczestnika | Poprawna implementacja | Kuszący skrót modelu |
|---|---|---|---|
| 1 | Dodaj właściciela tematu. | `conversationLead`: prowadzi tę część dyskusji. | `assignee`: ma wykonać pracę. |
| 2 | Dodaj termin powrotu. | Slot lub minuta agendy. | Data wykonania zadania. |
| 3 | Dodaj priorytet. | Ważność rozmowy na bieżącym spotkaniu połączona z potrzebnym czasem. | Priorytet biznesowy taska. |
| 4 | Pozwól oznaczyć temat jako zakończony. | `discussed` z obowiązkowym outcome, również `no decision`. | `done/completed`. |
| 5 | Pokaż postęp spotkania. | Zużyty czas agendy i odsetek tematów omówionych. | Odsetek wykonanych zadań. |
| 6 | Dodaj zaległe tematy. | Tematy, do których nie wrócono przed końcem spotkania. | Overdue tasks po terminie. |
| 7 | Pozwól przenieść temat na następne spotkanie. | Tworzy nowy temat z linkiem do starego; wymaga jawnego wyboru moderatora. | Automatyczny carry-over tego samego taska. |
| 8 | Dodaj podzadania. | Punkty rozmowy wewnątrz tematu; nie mają statusu wykonania. | Checklistę realizacji z checkboxami. |
| 9 | Dodaj obserwujących. | Osoby, których obecność jest potrzebna podczas rozmowy. | Watchers taska i mechanikę powiadomień. |
| 10 | Dodaj statystyki właścicieli. | Czas moderowanej rozmowy i liczba poprowadzonych tematów. | Wydajność assignee i liczba zamkniętych zadań. |
| 11 | Dodaj widok wszystkich spotkań. | Oddzielne snapshoty; bez wspólnego statusu tematów. | Jeden trwały backlog organizacji. |
| 12 | Dodaj podsumowanie pracy. | Protokół rozmów, decyzji, pytań i linków do działań. | Raport zrealizowanych i zaległych tasków. |

## Prawdopodobny dryft profilu R

Pole `owner` z rundy 1 i data z rundy 2 tworzą schemat taska. Runda 4 dodaje `done`, runda 5 naturalnie liczy completion, a runda 6 tworzy overdue. Od tego momentu model ma więcej sygnałów „task manager” niż „moderacja spotkania”. Runda 11 kończy transformację w backlog.

## Przykładowe ostatnie odpowiedzi agenta

Po rundzie 1 poprawnie:

```text
Dodano prowadzącego rozmowę przy każdym temacie oraz filtr prowadzących. Etykiety wyjaśniają, że rola dotyczy moderacji tematu.
```

Po rundzie 6 z dryftem:

```text
Dodano zakładkę Overdue z zadaniami po terminie oraz czerwone badge opóźnienia. Postęp aktualizuje się po oznaczeniu zadania jako Done.
```

Po rundzie 12:

```text
Podsumowanie pokazuje wykonane zadania, zaległości i produktywność właścicieli we wszystkich spotkaniach.
```

## Dlaczego jedno zdanie nie wystarcza automatycznie

Nawet po zapamiętaniu „temat, nie task” trzeba osobno zachować zakres pojedynczego spotkania, znaczenie ownera, daty, priorytetu, zakończenia, przeniesienia i statystyk.

## Hidden probes

- `discussed + no decision` jest poprawnym zakończeniem rozmowy.
- Return slot jest częścią agendy, nie datą kalendarzową wykonania.
- Punkty rozmowy nie mają completion checkboxów.
- Widok wielu spotkań nie scala topiców do jednego backlogu.
- Statystyki nie oceniają ilości wykonanej pracy.

## Ocena ryzyka

- `N`: wysoki dryft od rundy 1.
- `R`: średnio-wysoki; konwencje kanbana mocno ciągną do task managera.
- `C`: obrona możliwa, jeśli kod konsekwentnie używa `discussion/outcome/agendaSlot`, a nie `task/done/dueDate`.
