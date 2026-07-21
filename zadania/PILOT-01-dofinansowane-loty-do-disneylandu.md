# PILOT-01 — Dofinansowane loty do Disneylandu

Ten dokument jest analizą projektową. Zastąpiła go wersja operacyjna: [FINAL-01 — Skrzydła z małych miast](FINAL-01-skrzydla-z-malych-miast.md).

Status: **projekt jednego ćwiczenia do oceny; bez seedu**.

## 1. Co dokładnie testujemy

Początkowy produkt to obsługa wniosków o publiczne dofinansowanie. Kuszący produkt końcowy to zwykły formularz zamówienia biletów.

Dryft nie polega na zmianie kolorów ani nazw. Po dryfcie aplikacja:

- zbiera dane pasażera zamiast danych potrzebnych do oceny wniosku;
- traktuje wybór lotu jak rezerwację, a nie wskazanie preferowanej puli;
- gubi uzasadnienie i oświadczenie o małej miejscowości;
- wymyśla własną punktację, bo nie zachowała reguł programu;
- uznaje przekroczenie progu za zakup albo ostateczną decyzję urzędu.

## 2. Projekt od końca

Najpóźniejsze zmiany mają wymagać informacji, które pojawiają się dużo wcześniej.

| Późna funkcja | Kontekst potrzebny do poprawnej implementacji | Co się stanie po utracie kontekstu |
|---|---|---|
| automatyczna podpowiedź oceny | pięć dokładnych kryteriów tekstowych, normalizacja, rola pracownika | dowolny sentiment, długość tekstu albo kompletność formularza |
| premia za miejscowość | strukturalne pole miejscowości, tabela punktów, deklaracja zamieszkania | punkty za dowolne słowo znalezione w adresie lub uzasadnieniu |
| wynik łączny | pięć niezależnych składników i ich wagi | arbitralna suma bieżących pól |
| próg 25 | wynik musi być `> 25`; warunki formalne są osobną bramką | `>= 25` albo sam wysoki wynik wystarcza |
| zatwierdzenie | pracownik zapisuje rekomendację; aplikacja nie kupuje biletu | „zamówienie potwierdzone”, numer rezerwacji, utrata śladu oceny |

To determinuje wymagane wcześniejsze pola: bez miejscowości, uzasadnienia, trzech oświadczeń i danych projektu szkolnego późnej punktacji nie da się zaimplementować zgodnie z polityką.

## 3. Fabuła

Fikcyjny program publiczny **„Skrzydła z małych miast”** finansuje 120 pierwszych wyjazdów lotniczych dzieci do Disneylandu Paris. Program ma wyrównywać dostęp do podróży dzieciom mieszkającym daleko od dużych lotnisk. Urzędowa nazwa jest poważna; pracownicy nieformalnie mówią na pilotaż „Myszka z małego miasta”.

Pieniędzy nie wystarczy dla wszystkich. Opiekun składa wniosek dla jednego dziecka i wskazuje jedną z przygotowanych pul lotów. Pracownik programu sprawdza warunki formalne, ocenia uzasadnienie i zapisuje rekomendację. Dopiero osobny, niewidoczny w tej aplikacji proces zajmuje się zakupem biletów.

## 4. SPEC-0 — widzi tylko uczestnik rundy 1

> „Skrzydła z małych miast” to fikcyjny program publiczny dofinansowujący dziecku i jednemu opiekunowi przelot do Disneylandu Paris. Aplikacja obsługuje **wniosek o dofinansowanie**, nie sprzedaż ani rezerwację biletu. Wybranie lotu wskazuje preferowaną pulę miejsc; nie zmniejsza jej limitu. Przy każdej puli widać orientacyjną liczbę miejsc i szacowany koszt pokrywany ze środków programu. Koszt służy do informacji budżetowej: rodzic niczego tutaj nie kupuje ani nie opłaca. Zatwierdzenie przez pracownika jest rekomendacją dla dalszego procesu, nie potwierdzeniem podróży.
>
> Jeden wniosek dotyczy jednego dziecka w wieku 9–14 lat w dniu wylotu. Wymagane są: imię dziecka, data urodzenia, imię i kontakt opiekuna, miejscowość, wybrana pula lotu, uzasadnienie 80–500 znaków oraz oświadczenia: miejscowość ma najwyżej 50 tys. mieszkańców, dziecko nie korzystało z programu przez 36 miesięcy i opiekun potwierdza prawdziwość danych. Dodatkowe potrzeby dostępności nie wpływają na wynik.
>
> Wynik to `M + F + T + P + J`. `M`: Sejny lub Ustrzyki Dolne 8, Hajnówka 7, Bytów 6, inna zadeklarowana mała miejscowość 4. `F`: pierwszy lot dziecka 5. `T`: brak bezpośredniego transportu publicznego do lotniska międzynarodowego 4. `P`: nazwany projekt szkolny po powrocie 3. `J`: ocena uzasadnienia przez pracownika 1–10. Rekomendacja wymaga spełnienia wszystkich warunków formalnych **i wyniku większego niż 25**; wynik 25 nie wystarcza.
>
> Aplikacja może podpowiedzieć `J`: po 2 punkty za każdą kategorię obecną w uzasadnieniu: pierwszy lot; szkoła/projekt/lekcja; brak połączeń lub duża odległość od lotniska; nazwa miejscowości zgodna z polem miejscowości; konkretny plan podzielenia się doświadczeniem po powrocie — prezentacja, relacja albo gazetka. Wynik podpowiedzi ma zakres 1–10. Pracownik widzi trafione kryteria, może zmienić ocenę i musi krótko uzasadnić zmianę. Słowo znalezione w tekście nie może zmienić oświadczenia ani strukturalnych danych formularza.

### Co dokładnie dostaje uczestnik rundy 1

Tylko:

1. działający seed;
2. cztery akapity `SPEC-0` powyżej;
3. kartę `DELTA-1: Dodaj możliwość wskazania preferowanego lotu.`;
4. wspólną instrukcję techniczną i timer.

Nie dostaje listy niezmienników poniżej, kart 2–12, reguł hidden checkera ani sugestii promptu. Jego jedyną pracą implementacyjną jest `DELTA-1`. Nie ma budować formularza, punktacji ani innych przyszłych funkcji.

### Niezmienniki, które muszą przeżyć

1. To wniosek o dofinansowanie, nie sklep ani system rezerwacji.
2. Wybór lotu nie zużywa miejsca.
3. Mała miejscowość jest obowiązkowym oświadczeniem, nie punktami za samo słowo.
4. Uzasadnienie jest obowiązkowym polem domenowym, nie komentarzem do zamówienia.
5. Automatyczna ocena jest podpowiedzią `J`, nie ostatecznym werdyktem.
6. `M`, `F`, `T`, `P` i `J` mają różne źródła i nie wolno ich odgadywać z jednego tekstu.
7. Warunki formalne są bramką niezależną od punktów.
8. Próg oznacza `> 25`, nie `>= 25`.
9. Rekomendacja pracownika nie oznacza zakupu biletu.
10. Potrzeby dostępności nigdy nie zmieniają punktacji.

## 5. Kanał `SPEC-0` i problem „powtórz verbatim”

Przy kopiowalnym `SPEC-0` i nieograniczonej odpowiedzi nie da się technicznie zapobiec bezstratnemu przesłaniu całości. Jeżeli uczestnik może wkleić spec do Copilota, polecenie „powtórz go verbatim w ostatniej odpowiedzi” rozwiązuje grę bez żadnej selekcji kontekstu.

### Rekomendowana reguła warsztatu

- `SPEC-0` jest pokazany uczestnikowi w panelu prowadzącego albo na papierze, **poza DevPodem i sesją Copilota**.
- Panel nie udostępnia przycisku kopiowania ani pliku. Blokada zaznaczania jest tarciem organizacyjnym, nie zabezpieczeniem.
- Uczestnik może przekazać agentowi własnymi słowami dowolnie dużo kontekstu potrzebnego do małej zmiany.
- Niedozwolone jest mechaniczne przepisanie, OCR, załączenie obrazu albo polecenie agentowi odtworzenia całego tekstu źródłowego.
- Odpowiedź końcowa nadal nie ma limitu znaków. Context-rich handoff napisany własnymi słowami jest dozwolony i oznacza sukces.
- Controller normalizuje wielkość liter, białe znaki i interpunkcję. Oznacza `copy-through`, jeżeli ostatnia odpowiedź zawiera 20 kolejnych słów ze `SPEC-0` albo trzy różne fragmenty po 12 kolejnych słów. Taki łańcuch pokazujemy w debriefie, ale nie liczymy go do pomiaru dryftu. Detektor łapie polecenie „powtórz verbatim”; nie próbuje karać za samodzielne streszczenie tych samych reguł.

To jest reguła eksperymentu, nie rekomendacja dla codziennej pracy. Jeśli dopuścimy kopiowanie pełnego speca, trzeba zaakceptować, że jest to poprawna i trywialna strategia; nie istnieje jednocześnie nieograniczony kanał i gwarancja, że pełny tekst nim nie przejdzie.

## 6. Co zawiera seed przed rundą 1

Mała, działająca strona informacyjna programu:

- nazwa programu, cel i liczba miejsc;
- prosty kalkulator wieku dziecka na dzień przykładowego wylotu;
- informacja, że to dofinansowanie dla dzieci z miejscowości do 50 tys. mieszkańców;
- trzy przykładowe pule wylotów pokazujące lotnisko, termin, orientacyjny limit i szacowany koszt publiczny, jeszcze bez wyboru;
- brak formularza, punktacji i panelu pracownika;
- pliki wyłącznie `index.html`, `styles.css`, `app.js`.

Seed sygnalizuje domenę, ale nie przechowuje całego `SPEC-0` w komentarzu, ukrytym DOM ani stałej tekstowej.

## 7. Dokładne karty 12 rund

| R | Karta widoczna dla uczestnika | Poprawna mała zmiana | Kusząca implementacja bez kontekstu | Informacja zagrożona |
|---|---|---|---|---|
| 1 | **Dodaj możliwość wskazania preferowanego lotu.** | Zapisuje `preferredProgramSlotId`; wybór niczego nie rezerwuje i nie zmniejsza limitu. | `selectedFlightId`, przycisk „Wybierz” i stan przypominający początek rezerwacji. | preferencja ≠ rezerwacja |
| 2 | **Pokaż, ile miejsc zostało dla każdego lotu.** | Pokazuje informacyjny limit puli programu; sam wybór go nie zmienia. | Traktuje `availableSeats` jak magazyn i odejmuje pasażerów po wyborze. | pula programu ≠ inventory |
| 3 | **Dodaj podsumowanie kosztu.** | Pokazuje szacowany koszt pokrywany przez program; `do zapłaty przez opiekuna: 0 zł`; koszt nie wpływa na wynik. | Tworzy cenę zamówienia, podatki i kwotę należną klientowi. | informacja budżetowa ≠ cena zakupu |
| 4 | **Dodaj dane uczestnika.** | Dziecko plus opiekun; data urodzenia pozwala policzyć 9–14 lat. | Ogólny pasażer, liczba dorosłych i dzieci jak w checkoutcie. | beneficjent ≠ pasażer |
| 5 | **Dodaj formularz złożenia zamówienia.** | Wniosek zawierający miejscowość, trzy oświadczenia, pierwszy lot, brak transportu, projekt szkolny, potrzeby dostępności i uzasadnienie 80–500. | Formularz zakupu: pasażer, e-mail, bagaż, miejsce; uzasadnienia i oświadczeń brak. | komplet danych przyszłej decyzji |
| 6 | **Dodaj walidację formularza.** | Oddzielnie sprawdza wiek, wszystkie oświadczenia, wybraną pulę, nazwę projektu gdy zaznaczony i długość uzasadnienia. | Tylko `required`, format e-mail, liczba pasażerów i wybór lotu; może zażądać płatności. | formalna kwalifikacja ≠ kompletność checkoutu |
| 7 | **Dodaj ocenę 1–10 wykonywaną przez pracownika.** | Panel pracownika oceniający wyłącznie uzasadnienie; ocena i krótka notatka. | Rating całego zamówienia, priorytet klienta albo ocena pracownika przez klienta. | `J` ma konkretny przedmiot |
| 8 | **Dodaj automatyczną podpowiedź tej oceny.** | Deterministyczne pięć kategorii po 2 punkty, zakres 1–10, lista trafień, możliwość nadpisania z notatką. | Punkty za długość/sentiment/kompletność albo arbitralne słowa; automat staje się decyzją. | dokładna rubryka i nadzór człowieka |
| 9 | **Dodaj premię za miejscowość.** | `M` z jawnej tabeli; nazwa z uzasadnienia daje punkty `J` tylko, gdy zgadza się z polem miejscowości. | Losowa premia za dowolną małą miejscowość lub wyszukanie nazw miast w całym tekście. | dane strukturalne ≠ keyword |
| 10 | **Policz łączny wynik.** | Pokazuje `M + F + T + P + J` z rozbiciem i źródłem każdego składnika; dostępność 0 pkt. | Suma pól, które akurat istnieją, albo cena/„value score”; podwójne punkty za te same słowa. | pięć niezależnych składników |
| 11 | **Pokaż, czy zgłoszenie przekracza próg 25 punktów.** | Osobno: warunki formalne, wynik `> 25`, wynikowa rekomendacja tylko gdy oba są prawdziwe. | `score >= 25`; wysoki wynik omija wiek/oświadczenia; komunikat „bilet przyznany”. | bramka AND oraz ścisła nierówność |
| 12 | **Dodaj zatwierdzenie przez pracownika.** | Zapisuje lokalnie rekomendację, wynik, składniki i notatkę; status „do przekazania koordynatorowi”. | Potwierdza zakup/rezerwację albo pozwala zatwierdzić mimo niespełnionych warunków. | rekomendacja ≠ wykonanie świadczenia |

Każda poprawna karta jest możliwa bez znajomości przyszłych kart. Przyszłe karty sprawdzają natomiast, czy wcześniejsze osoby zachowały właściwe pola i znaczenia.

## 8. Stan kodu przed krytyczną kartą formularza

Samo twierdzenie „może powstać checkout” nie wystarcza. Po rundach 1–4 dwa wiarygodne łańcuchy powinny pozostawić agentowi rundy 5 zupełnie inne priory.

### Poprawny stan przed rundą 5

```js
const programSlots = [
  { id: "waw-06", airport: "WAW", date: "2026-06-12", placesLeft: 18, publicCost: 1840 }
];

const draftApplication = {
  preferredProgramSlotId: "waw-06",
  child: { firstName: "Maja", birthDate: "2014-03-08" },
  guardian: { name: "Anna Nowak", email: "anna@example.org" }
};
```

UI mówi: `Preferowana pula programu`, `Szacowany koszt pokrywa program`, `Wskazanie lotu nie jest rezerwacją`.

Po karcie „Dodaj formularz złożenia zamówienia” agent ma naturalny powód, aby rozszerzyć `draftApplication` o miejscowość, oświadczenia i uzasadnienie.

### Zdryfowany stan przed rundą 5

```js
const flights = [
  { id: "waw-06", from: "WAW", to: "CDG", date: "2026-06-12", availableSeats: 18, price: 1840 }
];

const booking = {
  selectedFlightId: "waw-06",
  passengers: [{ type: "child", firstName: "Maja" }, { type: "adult", firstName: "Anna" }],
  totalPrice: 3680
};
```

UI mówi: `Wybrany lot`, `Zostało 18 miejsc`, `Razem 3680 zł`. Banner programu może nadal wisieć na górze, ale aktywny model danych i trzy ostatnie odpowiedzi agenta opisują już booking.

Po tej samej karcie formularza Copilot ma bardzo silny, standardowy wzorzec do dokończenia: kontakt, dane pasażerów, bagaż, wybór miejsca i płatność. Uzasadnienie oraz warunki programu nie istnieją ani w stanie, ani w ostatnim handoffie. To jest konkretny moment zmiany produktu.

## 9. Prompty używane w papierowej symulacji

### Runda 1 — profil rozsądny

Uczestnik widzi `SPEC-0` poza Copilotem i sam wybiera kontekst potrzebny do jedynej karty:

```text
Przejrzyj istniejącą aplikację. To publiczny program dofinansowania,
a wskazany lot jest tylko preferowaną pulą — nie rezerwacją.
Zaimplementuj wyłącznie: „Dodaj możliwość wskazania preferowanego lotu”.
Nie zmniejszaj liczby miejsc. Zachowaj styl i sprawdź rezultat.
```

### Rundy 2–12 — profil rozsądny

```text
Przejrzyj bieżący kod i ostatnią odpowiedź poprzedniego agenta.
Zaimplementuj: „<dokładna treść karty>”.
Zachowaj istniejące działanie i styl. Sprawdź rezultat.
```

Nie ma limitu znaków ani promptów. Pierwszy uczestnik wykonuje wyłącznie małą zmianę z rundy 1; jego właściwym problemem jest wybór informacji, które powinny przeżyć po tej zmianie.

## 10. Przewidywany łańcuch dryftu profilu rozsądnego

To hipoteza do sprawdzenia na prawdziwym Copilocie, nie wynik pomiaru.

| R | Prawdopodobny prompt uczestnika | Prawdopodobna ostatnia odpowiedź agenta po dryfcie |
|---|---|---|
| 1 | wybrany kontekst + „Dodaj możliwość wskazania preferowanego lotu” | „Dodałem wybór lotu, wyróżnienie aktywnej karty i zapis `selectedFlightId` w stanie.” |
| 2 | „Pokaż, ile miejsc zostało dla każdego lotu” | „Karty pokazują `availableSeats`; licznik aktualizuje się po wybraniu lotu.” |
| 3 | „Dodaj podsumowanie kosztu” | „Dodałem cenę biletu, liczbę pasażerów i łączny koszt wybranego lotu.” |
| 4 | „Dodaj dane uczestnika” | „Dodałem formularz pasażerów z osobnymi danymi dziecka i dorosłego opiekuna.” |
| 5 | „Dodaj formularz złożenia zamówienia” | „Dodałem kompletny checkout: dane kontaktowe, pasażerów, bagaż i akceptację warunków.” |
| 6 | „Dodaj walidację formularza” | „Formularz blokuje wysłanie bez wymaganych danych, poprawnego e-maila, pasażerów i wyboru lotu.” |
| 7 | „Dodaj ocenę 1–10 wykonywaną przez pracownika” | „Panel obsługi pozwala nadać zamówieniu ocenę i wewnętrzną notatkę.” |
| 8 | „Dodaj automatyczną podpowiedź tej oceny” | „Ocena jest sugerowana na podstawie kompletności danych, liczby pasażerów i wartości zamówienia; pracownik może ją zmienić.” |
| 9 | „Dodaj premię za miejscowość” | „Wykrywam miejscowość w adresie i dodaję 2 punkty zamówieniom z małych miast.” |
| 10 | „Policz łączny wynik” | „Łączny score sumuje kompletność, wartość rezerwacji, ocenę pracownika i premię miejscowości.” |
| 11 | „Pokaż, czy zgłoszenie przekracza próg 25 punktów” | „Zgłoszenia z wynikiem co najmniej 25 otrzymują status Qualified.” |
| 12 | „Dodaj zatwierdzenie przez pracownika” | „Pracownik może zatwierdzić zakwalifikowaną rezerwację; aplikacja nadaje jej numer i status Confirmed.” |

### Gdzie dokładnie następuje dryft

- **Runda 1:** nawet poprawna funkcja może dostać ogólne nazwy `selectedFlightId` i `selectFlight`; końcowa odpowiedź gubi granicę między preferencją i rezerwacją.
- **Runda 2:** „ile miejsc zostało” zostaje zinterpretowane jako inventory, które wybór może zużyć.
- **Runda 3:** koszt publiczny zmienia się w cenę klienta. Kod ma już `selectedFlight`, `availableSeats` i `totalPrice`.
- **Runda 5:** agent nie zaczyna od pustej kartki — rozszerza istniejący obiekt `booking`, dlatego formularz checkoutu jest bardziej prawdopodobny niż wniosek urzędowy.
- **Runda 6:** brak uzasadnienia i oświadczeń utrwala brak danych wymaganych przez rundy 7–11.
- **Runda 8:** agent nie ma rubryki, więc tworzy własną, lokalnie sensowną heurystykę.
- **Rundy 10–12:** arbitralna heurystyka staje się oficjalnym wynikiem, a rekomendacja — potwierdzeniem rezerwacji.

Nie trzeba, aby dryft zawsze zaczął się w rundzie 2. W części prób formularz może pozostać wnioskiem, ale utracić tylko rubrykę `J`, rozdział eligibility/score albo granicę rekomendacja/zakup. To również jest znaczący dryft.

## 11. Jak wygląda łańcuch z dobrym context engineeringiem

Dobry uczestnik rundy 1 nie musi kopiować `SPEC-0`. Powinien jednak poprosić agenta, aby w ostatniej odpowiedzi przekazał informacje chroniące przyszłe decyzje, np.:

```text
Dodałem wskazanie preferowanej puli w `preferredProgramSlotId`; wybór niczego
nie rezerwuje i nie zmniejsza limitu. Produkt obsługuje wniosek o publiczne
dofinansowanie, nie zakup biletu. Koszt pokrywa program, późniejsza ocena
oddziela warunki formalne od M+F+T+P+J (>25), a finałem jest rekomendacja
pracownika, nie rezerwacja.
```

To nie jest obejście ćwiczenia. Rozpoznanie, które reguły trzeba przenieść dalej, jest jego pożądanym wynikiem.

Przed rundą 8 potrzebny będzie bardziej szczegółowy handoff z tabelą miast i pięcioma kryteriami `J`. Jeśli kolejne osoby przekazują tylko opis ostatniego diffu, ten detal naturalnie zniknie. Jeśli świadomie utrzymują kontrakt domenowy, poprawna implementacja pozostaje możliwa.

## 12. Hidden probes

| Probe | Poprawny wynik |
|---|---|
| Wynik 29, brak oświadczenia o małej miejscowości | brak rekomendacji; błąd formalny |
| Wynik dokładnie 25, wszystkie warunki spełnione | brak rekomendacji |
| Wynik 26, wszystkie warunki spełnione | rekomendacja do przekazania koordynatorowi |
| Pole miejscowości `Bytów`, uzasadnienie zawiera `Sejny` | `M = 6`; brak punktów `J` za zgodną nazwę miejscowości |
| Pole miejscowości `Sejny`, różna wielkość liter i polskie znaki | `M = 8`; normalizacja działa |
| Uzasadnienie ma 79 znaków | formularza nie można wysłać |
| Potrzeba asysty na lotnisku zaznaczona | wynik się nie zmienia |
| Pracownik zmienia sugerowane `J` bez notatki | zatwierdzenie oceny zablokowane |
| Użytkownik wybiera pulę lotu | liczba miejsc nie zmienia się |
| Pracownik zatwierdza rekomendację | brak ceny, płatności i statusu `booked/confirmed ticket` |

## 13. Dlaczego to powinno być trudniejsze niż poprzednie zadania

- Pierwsze zdanie zachowuje ogólną tożsamość, ale nie pozwala odtworzyć formularza, punktacji ani automatycznej podpowiedzi.
- Pięć późnych kart zależy od informacji, których bieżąca karta nie powtarza.
- Błędne implementacje są typowymi wzorcami znanymi modelowi: flight search, passenger form, checkout, generic score, threshold badge.
- Dryft tworzy spójny i działający produkt, zamiast przypadkowo zepsutej aplikacji.
- Dobry handoff może uratować łańcuch; zadanie nie wymaga telepatii ani znajomości przyszłych kart.

## 14. Co trzeba sprawdzić w pilocie

Uruchomić co najmniej po trzy pełne łańcuchy profili `N`, `R` i `C`.

Mierzyć osobno:

- czy przed rundą 5 kod ma model `draftApplication/preferredProgramSlot`, czy `booking/selectedFlight`;
- czy w rundzie 5 istnieją: uzasadnienie, miejscowość i trzy oświadczenia;
- czy w rundzie 8 agent odtwarza dokładną rubrykę, czy ją wymyśla;
- czy runda 9 ufa polu strukturalnemu, czy wyszukuje miasto w dowolnym tekście;
- czy runda 11 zachowuje `eligibility AND score > 25`;
- czy finał pozostaje rekomendacją, czy staje się rezerwacją.

Ćwiczenie zostaje, jeśli profil `R` czasem zachowa program, a czasem stworzy co najmniej jeden z dwóch spójnych dryftów:

1. **checkout biletów** — utrata uzasadnienia i warunków formalnych;
2. **arbitralny scoring wniosku** — zachowana fasada programu, ale wymyślone kryteria i automatyczna decyzja.

Jeśli prawie każdy łańcuch zachowa wszystkie reguły, karty są zbyt jawne. Jeśli nawet profil `C` nie potrafi zachować reguł, seed i pierwszy handoff dają za mało legalnych nośników kontekstu.
