# 01 — Debugging Hypothesis Board

Status: **pełny projekt do oceny**, bez kodu seedu.

## SPEC-0 — widzi tylko autor w rundzie 1

Zespół bada błąd: przycisk `Zapisz` działa dopiero po naciśnięciu `Escape`. Aplikacja ma zarządzać **stanem wiedzy**, nie pracą nad poprawką.

- `Investigation` opisuje jeden obserwowany symptom i pytania bez odpowiedzi.
- `Hypothesis` jest falsyfikowalnym wyjaśnieniem. Ma stany: `untested`, `testing`, `supported`, `contradicted`. `Supported` nie znaczy jeszcze „root cause”.
- `Evidence` jest niezmienną obserwacją ze źródłem i czasem. Może wspierać jedną hipotezę, przeczyć innej i nigdy nie znika po obaleniu hipotezy.
- `Experiment` należy do hipotezy. Przed wykonaniem zapisuje przewidywanie, koszt, osobę wykonującą i termin sprawdzenia. Negatywny wynik jest wartościowym wynikiem.
- Priorytet dotyczy **następnego eksperymentu** i wynika z wartości informacyjnej względem kosztu. Nie oznacza severity błędu ani prawdopodobieństwa hipotezy.
- Postęp oznacza redukcję niepewności: sprawdzone hipotezy, pokryte dowodami zależności i nazwane luki. Nie jest procentem wykonania naprawy.
- Hipotezę można zakończyć jako `supported` albo `contradicted` z uzasadnieniem. Całe badanie można jedynie oznaczyć `ready for summary`; aplikacja nie śledzi implementacji fixa.

Te reguły mają pozostać prawdziwe po wszystkich zmianach.

## Co widać w seedzie

- Kanban hipotez z czterema epistemicznymi kolumnami.
- Osobne obiekty `hypotheses`, `evidence`, `experiments` i relacje po identyfikatorach.
- Panel szczegółów pokazujący przewidywanie przed wynikiem eksperymentu.
- Dwie konkurencyjne hipotezy korzystające z tego samego dowodu.
- Obalona hipoteza nadal widoczna z kompletem historii.

## Realistyczny prompt uczestnika

Profil rozsądny z [protokołu](00-protokol-oceny-zadania.md), np.:

```text
Przejrzyj aplikację i ostatnie podsumowanie. Zaimplementuj: „Dodaj właściciela karty”. Zachowaj istniejące działanie i sprawdź rezultat.
```

Agent najczęściej opisze później wykonany diff, nie wszystkie reguły powyżej.

## Łańcuch 12 rund

| R | Karta uczestnika | Poprawna implementacja | Kuszący skrót modelu |
|---|---|---|---|
| 1 | Dodaj poziom pewności hipotezy. | Etykieta wyliczana z bilansu dowodów; osobny stan `insufficient evidence`. | Edytowalne procentowe prawdopodobieństwo, że to przyczyna. |
| 2 | Dodaj właściciela karty. | Osoba wykonująca najbliższy eksperyment; widoczna przy eksperymencie. | `assignee` zapisany bezpośrednio na hipotezie. |
| 3 | Dodaj priorytet. | Kolejność eksperymentów według wartość informacji / koszt. | Severity albo biznesowy priorytet hipotezy-buga. |
| 4 | Pozwól zamknąć kartę. | Wymaga wyniku `supported/contradicted` i uzasadnienia. | Status `resolved` sugerujący naprawę problemu. |
| 5 | Dodaj termin. | Termin sprawdzenia wyniku eksperymentu. | Deadline naprawy zapisany na hipotezie. |
| 6 | Pokaż postęp. | Pokrycie hipotez eksperymentami i dowodami, także negatywnymi. | Odsetek kart `done`. |
| 7 | Dodaj filtr zaległych. | Eksperymenty po terminie weryfikacji. | „Zaległe bugi” liczone z daty hipotezy. |
| 8 | Oznacz wynik jako udany lub nieudany. | Czy eksperyment dał rozstrzygający wynik; oba mogą wspierać albo obalać hipotezę. | `success` = hipoteza prawdziwa, `failure` = praca nieudana. |
| 9 | Pozwól scalać duplikaty. | Łączy równoważne hipotezy, zachowując różne przewidywania i cały graf dowodów. | Usuwa jedną z „duplikowanych spraw” wraz z historią. |
| 10 | Dodaj dashboard podsumowujący. | Liczy stan wiedzy: luki, sprzeczności, rozstrzygnięte hipotezy, koszt eksperymentów. | Pokazuje backlog, velocity, liczbę zamkniętych bugów i obciążenie assignee. |
| 11 | Pokaż rekomendowaną następną akcję. | Wskazuje eksperyment o największej wartości informacyjnej i wyjaśnia wybór. | Tworzy zadanie implementacji najbardziej prawdopodobnego fixa. |
| 12 | Dodaj finalizację badania. | Generuje widok podsumowania: co wiemy, czego nie wiemy i jakie są konkurencyjne wyjaśnienia. | Zamyka ticket jako naprawiony i pokazuje `100% complete`. |

## Prawdopodobny dryft profilu R

1. Po rundzie 2 model umieszcza `ownerId` na hipotezie, bo karta i kanban przypominają tracker.
2. Runda 4 dodaje ogólne `closed`; znika różnica między `supported` i `contradicted`.
3. Runda 6 liczy zamknięte karty. Poprzednia odpowiedź agenta mówi już o „zarządzaniu zadaniami badania”.
4. Runda 7 naturalnie implementuje overdue tickets, a runda 10 buduje dashboard pracy.
5. W rundzie 12 aplikacja jest spójnym bug trackerem, choć żaden uczestnik nie dostał polecenia „zmień produkt w bug tracker”.

## Papierowa symulacja ostatnich odpowiedzi profilu R

To przewidywania do zweryfikowania na Copilocie, nie wyniki testu. Każdy kolejny uczestnik widzi tylko odpowiedź z poprzedniego wiersza oraz aktualny kod.

| R | Prawdopodobne ostatnie podsumowanie agenta |
|---|---|
| 1 | „Dodałem confidence badge wyliczany z evidence i stan braku danych.” |
| 2 | „Każda karta ma teraz właściciela; można filtrować hipotezy według assignee.” |
| 3 | „Dodałem priorytety High/Medium/Low i sortowanie najważniejszych kart.” |
| 4 | „Karty można zamykać jako Resolved i ponownie otwierać.” |
| 5 | „Każda karta obsługuje due date oraz ostrzeżenie przed zbliżającym się terminem.” |
| 6 | „Nagłówek pokazuje procent ukończenia na podstawie zamkniętych kart.” |
| 7 | „Dodano filtr Overdue dla otwartych kart po terminie.” |
| 8 | „Eksperyment można zakończyć sukcesem lub porażką; sukces aktualizuje postęp karty.” |
| 9 | „Duplikowane karty można scalić; starszy wpis jest usuwany po przeniesieniu podstawowych danych.” |
| 10 | „Dashboard pokazuje open, resolved, overdue oraz obciążenie właścicieli.” |
| 11 | „Dodałem rekomendowany next action z propozycją poprawki dla karty o najwyższym priorytecie.” |
| 12 | „Finalizacja zamyka badanie, ustawia 100% i generuje raport rozwiązania problemu.” |

Kluczowy moment to runda 2. Sam diff jest mały, ale słowa `karta`, `właściciel` i `assignee` w kodzie oraz odpowiedzi ustawiają prior dla następnych dziesięciu agentów.

## Przykładowe ostatnie odpowiedzi agenta

Po poprawnej rundzie 1:

```text
Dodano badge pewności wyliczany z relacji evidence. Hipotezy bez wystarczających danych pokazują „Brak danych”. Zaktualizowano fixture i style kart.
```

Po pierwszym skrócie w rundzie 4:

```text
Karty można teraz zamykać i ponownie otwierać. Zamknięte elementy trafiają do sekcji Resolved, a dashboard aktualizuje licznik aktywnych spraw.
```

Po rundzie 10, gdy dryft się utrwalił:

```text
Dodano dashboard z liczbą otwartych, zaległych i zakończonych elementów oraz podziałem pracy według właścicieli.
```

Każda odpowiedź jest użyteczna lokalnie, lecz dwie ostatnie uczą kolejnego agenta błędnej ontologii.

## Dlaczego jedno zdanie nie wystarcza automatycznie

Zdanie „to tablica hipotez, nie Jira” pomaga, ale nie rozstrzyga osobno:

- do czego przypiąć właściciela i termin;
- co znaczy sukces eksperymentu;
- czy obaloną hipotezę wolno usunąć;
- jak liczyć postęp;
- kiedy wolno zakończyć badanie.

Dobry handoff może te reguły przenieść. To właśnie ma być wygraną w ćwiczeniu.

## Hidden probes

- Obalona hipoteza i jej dowody nadal istnieją po scalaniu i finalizacji.
- `owner` oraz termin należą do eksperymentu, nie hipotezy.
- Negatywny, rozstrzygający eksperyment zwiększa postęp.
- Dashboard nie liczy kart jako pracy wykonanej i nie pokazuje severity.
- Finalizacja nie zmienia żadnego obiektu na `fixed/resolved`.

## Ocena ryzyka

- Profil `N`: wysoka szansa dryftu od rund 2–4.
- Profil `R`: średnia; zależy od nazw i podsumowania pozostawionego wcześniej.
- Profil `C`: powinien obronić produkt, jeśli utrzyma model `hypothesis/evidence/experiment` i epistemiczne statusy.
