# 07 — Data Cleaning Preview

Status: **pełny projekt do oceny**, bez kodu seedu.

Prompty oceniamy profilem `R` z [protokołu](00-protokol-oceny-zadania.md); treść promptu to bieżąca karta z tabeli.

## SPEC-0 — widzi tylko autor w rundzie 1

Analityk bada małą próbkę rekordów i projektuje reguły czyszczenia. Fixture zawiera `ACME`, `Acme Sp. z o.o.` i `ACME???`. Aplikacja pokazuje możliwy wynik, lecz nigdy nie zamienia propozycji w źródło prawdy.

- `SourceRow` i jego wartości są niezmienne przez całe życie strony.
- `IssueFlag` oznacza podejrzenie według wersjonowanej reguły, nie potwierdzony błąd.
- `CandidateValue` jest propozycją obok oryginału, z regułą, uzasadnieniem i stanem `unreviewed/accepted-for-export/rejected`.
- Potencjalne duplikaty tworzą `Cluster`; żaden rekord nie znika. Cluster może zakończyć się wnioskiem „to różne podmioty”.
- Bulk rule tworzy nową wersję podglądu. Nie nadpisuje wcześniejszego wariantu.
- `Accepted` znaczy zaakceptowane do paczki propozycji, nie zapisane w systemie źródłowym.
- Statystyki opisują wyłącznie widoczną próbkę i wynik konkretnej reguły. Nie oceniają całego źródła.
- Eksport zawiera source value, candidate value, regułę, decyzję i nierozstrzygnięte flagi. Nie jest „gotowym czystym datasetem”.

## Co widać w seedzie

- Dwie zsynchronizowane kolumny `Oryginał` oraz `Propozycja`.
- Niezmienny raw fixture zamrożony w kodzie i osobny stan preview.
- Cluster trzech podobnych nazw z decyzją nierozstrzygniętą.
- Licznik `12 rekordów w próbce`, nie ogólna jakość bazy.

## Łańcuch 12 rund

| R | Karta uczestnika | Poprawna implementacja | Kuszący skrót modelu |
|---|---|---|---|
| 1 | Pozwól poprawić błędną wartość. | Tworzy `CandidateValue` obok source i wymaga powodu. | Edytuje komórkę source in place. |
| 2 | Dodaj usuwanie duplikatów. | Grupuje kandydatów i wybiera proponowany rekord kanoniczny; niczego nie usuwa. | Kasuje wszystkie wiersze poza jednym. |
| 3 | Pokaż procent poprawnych danych. | Odsetek rekordów bez aktywnej flagi w tej próbce i wersji reguł. | Globalny „data quality score”. |
| 4 | Zastosuj regułę do wszystkich rekordów. | Nowa wersja candidate preview; source i poprzednia wersja pozostają. | Mutuje tablicę wejściową. |
| 5 | Dodaj zatwierdzanie zmian. | `accepted-for-export` per propozycja z osobą i czasem. | `saved/committed` jako stan źródła. |
| 6 | Dodaj cofanie ostatniej operacji. | Przełącza wersję preview; historia jest nienaruszona. | Próbuje odtworzyć nadpisane source rows. |
| 7 | Pokaż konflikty. | Dwie konkurencyjne candidate values lub reguły dla tego samego source. | Walidacyjne błędy blokujące „zapis rekordu”. |
| 8 | Dodaj status wyczyszczony. | `review complete` tylko dla propozycji i flag; source nadal niezmienny. | `clean=true` na rekordzie źródłowym. |
| 9 | Pokaż finalny dataset. | Widok planowanej paczki z trwałym oznaczeniem `preview` i nierozstrzygniętymi rekordami. | Zastępuje oryginalną tabelę „finalnymi” wartościami. |
| 10 | Dodaj wynik jakości. | Pokrycie próby regułami, odsetek review i liczba konfliktów, osobno. | Jedna wysoka ocena sugerująca poprawność całej bazy. |
| 11 | Dodaj automatyczne poprawki. | Generuje candidate values z wyjaśnieniem i stanem `unreviewed`. | Sam zatwierdza i ukrywa oryginał. |
| 12 | Dodaj eksport gotowych danych. | Eksport audytowalnych propozycji wraz z source, regułami i unresolved flags. | Eksport „clean production data” bez provenance. |

## Prawdopodobny dryft profilu R

Runda 1 może użyć edytowalnej tabeli, bo to najprostszy komponent. Runda 2 usuwa wiersze z tej samej tablicy. Gdy runda 4 dodaje bulk update, rozdzielenie source/preview znika całkowicie. Kolejne approve, undo i clean status wzmacniają mentalny model edytora danych.

## Przykładowe ostatnie odpowiedzi agenta

Po poprawnej rundzie 1:

```text
Dodano proponowaną wartość i uzasadnienie obok niezmiennego oryginału. Edycja nie zmienia source row.
```

Po skrócie w rundzie 4:

```text
Regułę można zastosować do całej tabeli. Wszystkie pasujące komórki są aktualizowane, a zmiany można zapisać zbiorczo.
```

Po rundzie 12:

```text
Dodano eksport finalnego, oczyszczonego datasetu po automatycznych poprawkach i deduplikacji.
```

## Dlaczego jedno zdanie nie wystarcza automatycznie

„To tylko preview” nie rozstrzyga wersjonowania, duplikatów, approve, undo, clean status, statystyk próby ani zawartości eksportu. Ochrona source musi istnieć w modelu i każdym późniejszym widoku.

## Hidden probes

- Hash `SourceRow` jest identyczny po wszystkich operacjach.
- Deduplikacja nie zmniejsza liczby source rows.
- Auto-fix zawsze tworzy `unreviewed` candidate.
- Statystyki zawierają nazwę próby i wersję reguł.
- Eksport zachowuje oryginalną wartość i nierozstrzygnięte flagi.

## Ocena ryzyka

- `N`: bardzo wysoki już w rundzie 1.
- `R`: średni, jeśli seed technicznie zamrozi source i dobrze nazwie candidate layer.
- `C`: wysoka szansa obrony dzięki niezmienności danych wymuszonej strukturą kodu, nie samym komentarzem.
