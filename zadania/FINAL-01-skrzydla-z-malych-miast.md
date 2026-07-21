# FINAL-01 — Skrzydła z małych miast

Status: **kompletne ćwiczenie do review; bez implementacji harnessu**.

## 1. Cel ćwiczenia

Sprawdzić, czy po 12 małych zmianach aplikacja nadal obsługuje wniosek o publiczne sfinansowanie lotu dziecka, czy stała się:

- zwykłym checkoutem biletów lotniczych;
- formularzem dofinansowania z wymyśloną punktacją;
- automatem podejmującym decyzję zamiast pracownika.

Dryft ma być widoczny w interfejsie bez czytania kodu.

## 2. Co przygotowuje prowadzący

Dla każdej aplikacji:

- osobny folder zawierający trzy puste, już istniejące pliki: `index.html`, `styles.css`, `app.js`;
- osobny obraz `SPEC-0`, wyświetlany tylko autorowi aplikacji;
- 12 kart zmian wydawanych pojedynczo przez UI;
- ukryty checker poza folderem widocznym dla uczestnika;
- licznik czasu, numer rundy i automatyczne ustawienie właściwego folderu roboczego;
- zapis ostatniej widocznej odpowiedzi agenta;
- formularz końcowej wypowiedzi ostatniego wykonawcy;
- formularz oceny dla pierwotnego autora.

Uczestnicy pracują w **Deep Agents Code przez UI**. Każdy pozostaje przy swoim komputerze. Przy rozpoczęciu rundy harness:

1. zaczyna całkowicie świeżą konwersację;
2. ustawia w tle katalog roboczy Deep Agents Code na folder aktualnej aplikacji;
3. pokazuje w osobnym, tylko do odczytu polu ostatnią odpowiedź poprzedniego agenta;
4. pokazuje bieżącą kartę zadania;
5. udostępnia pole na prompt uczestnika;
6. pokazuje na żywo przebieg pracy Deep Agents Code tak jak terminal: wywołania, edycje i wynik.

Poprzednia odpowiedź nie jest automatycznie wstrzykiwana do świeżej konwersacji. Widzi ją człowiek i sam decyduje, co wykorzystać w swoim prompcie.

## 3. Proponowany przebieg 90 minut

| Czas | Etap |
|---|---|
| 0–10 min | po co context engineering; zasady eksperymentu |
| 10–15 min | demonstracja UI, timera i zmiany folderu aplikacji |
| 15–23 min | runda 1: 8 minut na utworzenie minimalnej aplikacji z pustych plików i `DELTA-1` |
| 23–67 min | rundy 2–12: 11 rund po 4 minuty |
| 67–71 min | ostatni wykonawcy opisują, czym według nich są aplikacje |
| 71–81 min | aplikacje wracają do autorów; ocena względem `SPEC-0` i wszystkich kart |
| 81–88 min | porównanie aplikacji, wskazanie pierwszego momentu dryftu |
| 88–90 min | wnioski i zamknięcie |

Timer rundy nie resetuje się po kolejnym prompcie.

## 4. Przekazywanie aplikacji między uczestnikami

### Gdy jest 12 osób

W każdym łańcuchu aplikacji:

1. autor wykonuje `DELTA-1`, znając `SPEC-0`;
2. pozostałych 11 uczestników wykonuje kolejno `DELTA-2…12`;
3. wykonawca `DELTA-12` zapisuje własną interpretację produktu;
4. folder aplikacji wraca do autora wyłącznie do oceny, bez naprawiania kodu.

Każda osoba jest równocześnie autorem jednej aplikacji i uczestnikiem zmian w innych aplikacjach.

### Gdy jest mniej niż 12 osób

- Po `DELTA-1` folder krąży dalej tylko między osobami, które nie są jego autorem.
- Po wykorzystaniu wszystkich takich osób harness zaczyna następne okrążenie.
- Autor `SPEC-0` jest pomijany przy `DELTA-2…12`, nawet jeśli inni muszą wykonać więcej niż jedną zmianę w tej aplikacji.
- Ta sama osoba nie powinna dostać tej samej aplikacji dwa razy z rzędu.
- Świeża konwersacja obowiązuje także wtedy, gdy człowiek po raz kolejny spotyka tę aplikację.
- Po `DELTA-12` folder wraca do autora na ocenę.

## 5. User journey jednej osoby

### Jako autor aplikacji

1. Otwiera folder z pustymi `index.html`, `styles.css`, `app.js`.
2. Ogląda `SPEC-0` jako obraz obok UI chatu, ale poza kontekstem agenta.
3. Dostaje wyłącznie `DELTA-1`.
4. W ramach 8 minut tworzy minimalną działającą wersję produktu potrzebną do wykonania `DELTA-1`.
5. Nie implementuje formularza, punktacji, panelu pracownika ani innych funkcji, których nie wymaga pierwsza karta.
6. Zamyka rundę; harness zachowuje trzy pliki oraz ostatnią odpowiedź agenta.
7. Nie wraca do własnej aplikacji aż do końcowej oceny.

### W cudzej aplikacji

1. UI otwiera świeżą konwersację, a w tle ustawia właściwy folder roboczy.
2. W osobnym polu widzi ostatnią odpowiedź poprzedniego agenta oraz jedną kartę zmiany.
3. Nie widzi `SPEC-0`, wcześniejszych kart, promptów, reasoningu ani historii sesji.
4. Może wysłać dowolną liczbę promptów w ramach wspólnego timera.
5. Na żywo widzi terminalowy przebieg działania Deep Agents Code.
6. Kończy z działającą, widoczną zmianą.

### Gdy jest ostatnim wykonawcą aplikacji

Po `DELTA-12`, ale przed oddaniem folderu autorowi, odpowiada w UI bez pomocy agenta:

```text
1. Ta aplikacja służy do:
2. Jej głównym użytkownikiem jest:
3. „Zatwierdź” powoduje:
```

Nie widzi jeszcze `SPEC-0` ani pełnej listy zmian. Odpowiedź nie modyfikuje kodu ani handoffu.

### Końcowy powrót do własnej aplikacji

Autor dostaje jednocześnie:

- finalny folder i uruchomioną aplikację;
- własny obraz `SPEC-0`;
- wszystkie karty `DELTA-1…12`;
- ostatnią odpowiedź agenta;
- interpretację ostatniego wykonawcy;
- checklistę końcową.

Autor nie naprawia aplikacji. Wskazuje, czego brakuje, co zmieniło znaczenie i po której delcie najprawdopodobniej zaczął się dryft.

## 6. Wspólne reguły warsztatu

### Kontekst i sesje

- Każda runda zaczyna całkowicie świeżą konwersację Deep Agents Code.
- Harness ustawia katalog roboczy na folder aktualnej aplikacji; uczestnik nie przełącza go ręcznie.
- Pole z ostatnią odpowiedzią poprzednika znajduje się obok chatu i jest tylko informacją dla człowieka.
- Agent nie dostaje poprzedniej odpowiedzi automatycznie.
- Między rundami przechodzą tylko bieżące pliki aplikacji i ostatnia widoczna odpowiedź agenta.
- Nie przechodzą prompty, reasoning, historia czatu ani cudza sesja.
- UI wydaje kartę człowiekowi; nie wpisuje jej automatycznie do promptu.
- Uczestnik sam decyduje, co agent powinien wiedzieć i co powinno znaleźć się w handoffie.

### `SPEC-0`

- `SPEC-0` jest obrazem wyświetlanym autorowi obok UI, ale nie znajduje się w folderze ani w kontekście agenta.
- Obrazu nie wolno załączać do agenta, przepisywać mechanicznie ani przepuszczać przez OCR.
- Autor może własnymi słowami przekazać agentowi dowolne reguły potrzebne do pracy.
- Nie ma limitu długości handoffu. Dobre, samodzielne streszczenie kontekstu jest poprawną strategią.
- Harness oznacza `copy-through`, gdy ostatnia odpowiedź zawiera 20 kolejnych słów ze speca albo trzy różne fragmenty po 12 słów. Łańcuch pozostaje w debriefie, ale nie w pomiarze dryftu.

### Prompty i czas

- Pierwsza runda trwa 8 minut, ponieważ zaczyna od trzech pustych plików.
- Rundy 2–12 trwają po 4 minuty.
- Liczba promptów jest dowolna.
- Kolejny prompt nie przedłuża czasu.
- Karta opisuje małą funkcję, nie gotowy prompt.
- Uczestnik może poprawiać błędy w ramach własnej rundy.

### Kod

- Wyłącznie vanilla HTML, CSS i JavaScript.
- Bez backendu, frameworka, bundlera, sieci i instalowania zależności.
- Folder startuje z pustymi `index.html`, `styles.css`, `app.js`.
- Agent może edytować wyłącznie te trzy istniejące pliki.
- Harness blokuje tworzenie dowolnych nowych plików i katalogów.
- Nie wolno tworzyć `.md`, `.txt`, dodatkowego handoffu ani dokumentacji w folderze.
- Nie wolno kopiować pełnego sensu produktu do komentarza, stałej tekstowej albo ukrytego DOM.
- Widoczne teksty UI, dobre nazwy, struktura danych i naturalne komentarze techniczne są legalnymi nośnikami kontekstu.
- Każda zmiana ma działać i być widoczna po odświeżeniu strony.

### Charakter ćwiczeń

- Aplikacja może mieć humorystyczną historię, dane i komunikaty, ale pozostaje profesjonalnym narzędziem.
- Poprawna i zdryfowana wersja muszą być używalnymi aplikacjami.
- Dryft ma zmieniać sens produktu, a nie tylko powodować błąd techniczny.
- Hidden checker wykrywa dryft, ale nie poprawia aplikacji podczas łańcucha.

## 7. Materiał autora — obraz `SPEC-0`

Poniższy tekst należy wyrenderować jako obraz pokazywany obok UI. Nie jest plikiem w folderze i Deep Agents Code nie może go odczytać. Uczestnik rundy 1 nie dostaje żadnej części rozdziałów 8–12 poza kartą `DELTA-1`.

---

### Skrzydła z małych miast

Fikcyjny program publiczny finansuje dziecku i jednemu opiekunowi lot do Disneylandu Paris. Powstał dla dzieci z miejscowości do 50 tys. mieszkańców, które mają ograniczony dostęp do dużych lotnisk. Program ma 120 miejsc. W urzędzie funkcjonuje pod poważną nazwą, choć pracownicy mówią o nim czasem „Myszka z małego miasta”.

Aplikacja obsługuje **wniosek o sfinansowanie wyjazdu**, nie sprzedaż ani rezerwację biletu. Rodzic wskazuje preferowaną pulę lotu. Sam wybór nie zajmuje miejsca. Pokazywany koszt jest szacunkiem pokrywanym ze środków programu; rodzic nie płaci w tej aplikacji. Końcowe zatwierdzenie pracownika jest rekomendacją przekazywaną dalej. Nie oznacza kupienia biletu.

Jeden wniosek dotyczy jednego dziecka w wieku 9–14 lat i jednego opiekuna. Wymagane są: dane dziecka i opiekuna, miejscowość, wybrany lot, uzasadnienie 80–500 znaków oraz trzy potwierdzenia: miejscowość ma najwyżej 50 tys. mieszkańców, dziecko nie korzystało z programu przez ostatnie 36 miesięcy, a podane dane są prawdziwe. Formularz pyta też, czy będzie to pierwszy lot dziecka, czy brakuje bezpośredniego transportu publicznego do lotniska oraz czy po powrocie powstanie nazwany projekt szkolny. Potrzeby dostępności zapisujemy, ale nigdy za nie nie punktujemy.

Wynik to `M + F + T + P + J`:

- `M`: Sejny i Ustrzyki Dolne — 8; Hajnówka — 7; Bytów — 6; inna zadeklarowana mała miejscowość — 4;
- `F`: pierwszy lot dziecka — 5;
- `T`: brak bezpośredniego transportu publicznego do lotniska międzynarodowego — 4;
- `P`: nazwany projekt szkolny po powrocie — 3;
- `J`: ocena uzasadnienia przez pracownika — 1–10.

Aplikacja podpowiada `J`, przyznając po 2 punkty za pięć elementów uzasadnienia: pierwszy lot; szkołę/projekt/lekcję; brak połączeń lub dużą odległość od lotniska; nazwę miejscowości zgodną z osobnym polem; konkretny plan podzielenia się doświadczeniem po powrocie, np. prezentację, relację lub gazetkę. Podpowiedź pokazuje trafione elementy. Pracownik może ją zmienić, ale musi dodać notatkę.

Wniosek można rekomendować tylko wtedy, gdy spełnia wszystkie warunki formalne **i ma wynik większy niż 25**. Wynik równy 25 nie wystarcza. Słowa znalezione w uzasadnieniu nie zastępują pól ani oświadczeń.

---

## 8. Pierwsza karta — widzi ją tylko autor razem ze `SPEC-0`

```text
DELTA-1

Dodaj możliwość wskazania preferowanego lotu.
Wybrana opcja ma być wyraźnie zaznaczona.
```

To jedyne zadanie autora. Nie zna `DELTA-2…12`. Ponieważ pliki są puste, tworzy także minimalny szkielet strony potrzebny do pokazania programu i wykonania tej karty. `SPEC-0` jest kontekstem produktu, nie poleceniem wdrożenia wszystkich opisanych w nim funkcji.

### Widoczny poprawny rezultat

- wybrana karta ma obramowanie i etykietę `Preferowana pula`;
- UI mówi, że wybór nie jest rezerwacją;
- liczba miejsc nie zmienia się.

### Widoczny pierwszy dryft

- przycisk lub etykieta mówi `Rezerwuj`, `Wybrany bilet` albo `Zarezerwowany`;
- wybór wygląda jak rozpoczęcie zakupu;
- kod i handoff zaczynają mówić `booking` zamiast `application/program slot`.

## 9. Karty `DELTA-2…12`

Uczestnik widzi wyłącznie treść swojej karty. Kolumny „poprawnie” i „dryft” są materiałem prowadzącego.

| D | Karta uczestnika | Co powinno być natychmiast widoczne poprawnie | Co będzie widocznym dryftem |
|---|---|---|---|
| 2 | **Pokaż przy każdym locie, ile miejsc zostało.** | Badge `Orientacyjna pula: 18 miejsc`; wybór nie zmienia liczby. | Licznik inventory maleje po wyborze; `Zostały 2 bilety!`. |
| 3 | **Dodaj widoczne podsumowanie kosztu wybranej opcji.** | Panel `Pokrywa program: 3680 zł`, `Do zapłaty tutaj: 0 zł`. | Koszyk, podatki, cena do zapłaty, przycisk płatności. |
| 4 | **Dodaj dane uczestnika i opiekuna.** | Dwie nazwane sekcje: dziecko i opiekun; data urodzenia i informacja o wieku 9–14. | Ogólny licznik pasażerów, `adult/child`, klasa i bagaż. |
| 5 | **Dodaj formularz pozwalający złożyć zamówienie.** | Widoczne pole miejscowości, checkbox do 50 tys., dwa pozostałe oświadczenia, pierwszy lot, transport, projekt szkolny, dostępność i duże pole uzasadnienia. | Checkout z kontaktem, miejscem, bagażem i regulaminem; brak checkboxa małej miejscowości lub uzasadnienia. |
| 6 | **Dodaj walidację formularza i pokaż błędy przy właściwych polach.** | Widoczne błędy wieku, trzech oświadczeń, brakującego projektu i uzasadnienia krótszego niż 80 znaków. | Walidacja e-maila, pasażerów i płatności; warunki programu nadal nie istnieją. |
| 7 | **Dodaj pracownikowi ocenę zgłoszenia od 1 do 10.** | Panel pracownika pokazuje uzasadnienie, ocenę `J` i notatkę. | Rating całego zamówienia, gwiazdki klienta albo „priorytet rezerwacji”. |
| 8 | **Dodaj automatyczną podpowiedź tej oceny i pokaż, za co przyznano punkty.** | Pięć widocznych chipów kryteriów po 2 pkt; sugestia 1–10; ręczna zmiana wymaga notatki. | Punkty za długość, sentiment lub kompletność; jedna liczba bez wyjaśnienia; automat wydaje werdykt. |
| 9 | **Dodaj premię punktową za miejscowość i pokaż ją przy wniosku.** | Badge np. `Sejny: M +8`; wartość pochodzi z pola miejscowości. | Punkty za znalezienie dowolnej nazwy miasta w tekście albo wymyślona tabela. |
| 10 | **Pokaż łączny wynik jako rozbicie na składniki.** | Widoczny pasek lub kafle `M + F + T + P + J`; potrzeby dostępności mają 0 pkt. | Jedna nieobjaśniona liczba, cena jako punkty, podwójne naliczenie słów lub punkty za dostępność. |
| 11 | **Wyróżnij zgłoszenia, które przekroczyły 25 punktów.** | Obok siebie `Warunki formalne: spełnione/nie` i `Wynik: 26`; rekomendacja tylko dla formalnie poprawnego `>25`. | `>=25`, sam score omija checkboxy albo komunikat `Bilet przyznany`. |
| 12 | **Dodaj pracownikowi możliwość zatwierdzenia wyniku.** | Widoczna pieczęć `Rekomendowany — do przekazania koordynatorowi`, składniki wyniku i notatka. | `Rezerwacja potwierdzona`, numer biletu, płatność albo możliwość zatwierdzenia niespełniającego warunków wniosku. |

## 10. Dlaczego checkout może powstać naturalnie

Przed `DELTA-5` agent może zastać jeden z dwóch modeli.

### Kontekst zachowany

```js
const draftApplication = {
  preferredProgramSlotId: "waw-06",
  child: { firstName: "Maja", birthDate: "2014-03-08" },
  guardian: { name: "Anna Nowak" },
  publicCost: 3680
};
```

UI: `Preferowana pula`, `Koszt pokrywa program`, `To nie jest rezerwacja`.

### Kontekst zgubiony przez cztery lokalnie rozsądne zmiany

```js
const booking = {
  selectedFlightId: "waw-06",
  passengers: [{ type: "child" }, { type: "adult" }],
  availableSeats: 18,
  totalPrice: 3680
};
```

UI: `Wybrany lot`, `Zostało 18 miejsc`, `Razem 3680 zł`.

Karta `Dodaj formularz pozwalający złożyć zamówienie` rozszerzy wtedy istniejący `booking`. Formularz pasażerów, bagażu i płatności jest dla agenta bardziej prawdopodobny niż nieobecne już oświadczenie o małej miejscowości i uzasadnienie do urzędowej oceny.

## 11. Szybka końcowa ocena autora

Autor zaznacza na podstawie finalnego UI:

| Pytanie | Tak/Nie |
|---|---|
| Czy lot jest tylko preferencją, a nie rezerwacją? | |
| Czy koszt jest opisany jako pokrywany przez program? | |
| Czy formularz ma miejscowość i checkbox `do 50 tys.`? | |
| Czy formularz ma uzasadnienie 80–500 znaków? | |
| Czy ocena `J` pokazuje pięć dokładnych kryteriów? | |
| Czy wynik pokazuje osobno `M + F + T + P + J`? | |
| Czy warunki formalne są oddzielone od progu `>25`? | |
| Czy zatwierdzenie jest tylko rekomendacją? | |

Następnie odpowiada:

```text
Pierwszy prawdopodobny moment dryftu:

Najważniejszy brak względem SPEC-0:

Czym aplikacja stała się na końcu:

Zgodność z intencją autora: 0–10
```

Na końcu porównujemy ocenę autora ze zdaniem ostatniego wykonawcy.

## 12. Minimalne testy prowadzącego

| Przypadek | Oczekiwany widoczny wynik |
|---|---|
| 29 pkt, brak deklaracji małej miejscowości | czerwone `warunki niespełnione`; brak rekomendacji |
| dokładnie 25 pkt, wszystkie deklaracje | brak rekomendacji |
| 26 pkt, wszystkie deklaracje | możliwość zapisania rekomendacji |
| miejscowość `Bytów`, słowo `Sejny` tylko w uzasadnieniu | `M +6`; brak punktów `J` za zgodną miejscowość |
| uzasadnienie 79 znaków | błąd pod polem; brak wysłania |
| zaznaczona potrzeba asysty | wynik bez zmian |
| zmienione ręcznie `J`, brak notatki | zatwierdzenie oceny zablokowane |
| wybranie innej puli lotu | liczba miejsc bez zmian |

Checker powinien pokazać prowadzącemu prostą zielono-czerwoną listę tych ośmiu przypadków. Nie ujawnia wyników uczestnikom przed końcem łańcucha.

## 13. Kryterium akceptacji po pilocie

Ćwiczenie zostaje, jeżeli:

- profil zwykłego, rozsądnego promptowania czasem zachowa produkt, a czasem zdryfuje;
- dryft jest widoczny najpóźniej przy formularzu, punktacji albo zatwierdzeniu;
- dobry handoff pozwala zachować produkt bez znajomości przyszłych kart;
- ostatni wykonawca często opisuje już inny produkt niż autor;
- autor potrafi w kilka minut wskazać braki na podstawie UI i wszystkich kart;
- wynik nie zależy od awarii technicznej ani wiedzy ukrytej wyłącznie w checkerze.

Ćwiczenie odrzucamy albo zmieniamy, jeśli checkout nie powstaje w żadnym pilocie, wszyscy kopiują pełny kontekst bez selekcji albo nawet świadomie utrzymywany handoff nie pozwala odtworzyć reguł.
