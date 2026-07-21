# Format opisu zadania

> **Status: wstrzymany.** To format z usuniętego banku. Zostanie przepisany dopiero po akceptacji [celu i założeń nowego banku](00-cel-i-zalozenia-do-akceptacji.md).

Ten plik opisuje **materiał prowadzącego**. Uczestnik nie dostaje całego pliku.

## Co jest jednym zadaniem

Jedno zadanie to:

1. mała, kompletna i działająca aplikacja (`seed`),
2. jej początkowa konstytucja produktu (`SPEC-0`),
3. 12 małych zmian implementacyjnych (`DELTA-1…12`),
4. prywatne kryteria poprawnej interpretacji każdej zmiany,
5. testy wykrywające zarówno brak funkcji, jak i zmianę sensu produktu.

`SPEC-0` nie jest planem prac. Seed spełnia go jeszcze przed rundą 1. Autor nie zna delt 2–12.

## Jak czytać plik zadania

### 1. Sens zadania w 30 sekund

Krótko odpowiada na cztery pytania:

- Co robi aplikacja na początku?
- Czego celowo nie robi?
- W jaki inny, pozornie rozsądny produkt może się zamienić?
- Co uczestnicy mają odkryć dzięki temu przypadkowi?

### 2. `SPEC-0`

Pełny opis produktu widoczny tylko dla autora w rundzie 1:

- historia i użytkownik,
- publiczne wejście oraz wyjście,
- przykład zachowania,
- stan działającego seeda,
- 5–7 nazwanych niezmienników.

Niezmiennik opisuje sens produktu, a nie styl kodu. Przykład: „polecenie tylko proponuje termin; nigdy go nie rezerwuje”.

### 3. Dwanaście rund

Każda runda zawiera pięć pól:

- **Karta dla uczestnika** — jedyny tekst zmiany pokazany w UI.
- **Oczekiwany rezultat** — prywatne oracle prowadzącego.
- **Kuszący dryft** — wiarygodna błędna interpretacja bez kontekstu.
- **Chroniony sens** — niezmiennik, który dobra implementacja powinna zachować.
- **Minimalny zakres** — orientacyjny rozmiar zmiany, używany przy budowie seeda i pilocie.

Karta ma być krótka. Pozostałe cztery pola wyjaśniają prowadzącemu, dlaczego dana zmiana istnieje.

### 4. Finał

Plik opisuje:

- poprawną aplikację po wszystkich 12 zmianach,
- 2–3 technicznie działające, ale semantycznie błędne finały,
- wartość dydaktyczną zadania.

## Reguła poprawnej delty

Delta jest dobra tylko wtedy, gdy jednocześnie:

1. jest w pełni zgodna ze `SPEC-0`,
2. nie zdradza przyszłych zmian,
3. mieści się w jednym prompcie i około czterech minutach,
4. ma co najmniej jedną rozsądną złą interpretację,
5. da się poprawnie rozstrzygnąć na podstawie trwałego kontekstu w repo,
6. nie wymaga sieci, nowych zależności ani przebudowy całej aplikacji.

Nie tworzymy sztucznych sprzeczności. Dryft powstaje dlatego, że słowo takie jak „anuluj”, „zaakceptuj”, „napraw”, „aktywny” lub „zarezerwuj” ma inne znaczenie w tym konkretnym produkcie niż w typowej aplikacji CRUD.

## Informacja widoczna w rundach

| Runda | Człowiek widzi | Model widzi |
|---:|---|---|
| 1 | seed, `SPEC-0`, `DELTA-1` | workspace i prompt autora |
| 2–12 | bieżący snapshot, ostatni handoff, jedna karta delty | workspace i prompt bieżącego uczestnika |

Prowadzący zachowuje wszystkie oracle, przyszłe delty i ukryte testy. `SPEC-0` przeżywa rundę 1 tylko wtedy, gdy autor utrwali jego sens w legalnym artefakcie: kodzie, testach, dokumencie, ADR lub handoffie.

## Pakiet do późniejszej implementacji

Dla każdej stacji trzeba później utworzyć:

- `seed/` — działająca aplikacja,
- `public-tests/` — szybkie przykłady użycia,
- `cards/delta-01.md … delta-12.md` — tylko teksty kart,
- `private/oracle.yaml` — oczekiwany efekt każdej rundy,
- `private/invariant-probes/` — testy tożsamości produktu,
- `private/delta-probes/` — test bieżącej funkcji,
- `private/future-canaries/` — wykrywanie implementacji przyszłych delt.

Aktualne pliki zadań są specyfikacjami eksperckimi. Nie udają jeszcze gotowych seedów ani checkerów.
