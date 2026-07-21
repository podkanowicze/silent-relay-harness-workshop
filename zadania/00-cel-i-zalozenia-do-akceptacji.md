# Cel i założenia nowego banku — do akceptacji

Status: **założenia przyjęte; powstało 12 pełnych łańcuchów do oceny**. [Otwórz bank zadań](README.md).

## 1. Co warsztat ma udowodnić

Agent nie dziedziczy intencji produktu. W tym eksperymencie kolejna osoba dostaje celowo tylko działający kod aplikacji oraz ostatnią odpowiedź agenta. Sens produktu musi więc przeżyć w zachowaniu, strukturze i nazewnictwie kodu albo w naturalnym podsumowaniu pracy.

Po 12 lokalnie rozsądnych zmianach aplikacja może nadal działać, ale służyć do czegoś innego niż na początku. Warsztat ma pokazać, że context engineering to utrzymywanie **sensu produktu i granic decyzji**, a nie samo pisanie dokładniejszych promptów.

Na końcu porównujemy:

- jedno zdanie autora: „ta aplikacja służy do…”;
- rzeczywiste zachowanie końcowego programu;
- jedno zdanie ostatniego uczestnika;
- rundę, w której pierwszy raz zmienił się sens produktu.

## 2. Jednostka eksperymentu

Przy 12 osobach:

- działa 12 równoległych łańcuchów z 12 różnymi, małymi aplikacjami;
- każdy folder zaczyna z trzema pustymi, istniejącymi plikami: `index.html`, `styles.css`, `app.js`;
- autor tworzy minimalną aplikację i realizuje pierwszą małą zmianę w dłuższej rundzie 1;
- odbywa się 12 rund, więc każdą aplikację zmienia 12 osób;
- każdy pracuje na swoim komputerze i we własnym dostępie do agenta; nie routujemy zapytań przez konto innego uczestnika;
- każda runda używa świeżej sesji agenta;
- między rundami przechodzi wyłącznie kod aplikacji i ostatnia odpowiedź agenta, nie historia czatu, prompty, reasoning ani cudza sesja;
- jedynym limitem liczby promptów jest timer rundy.

Po ostatniej zmianie wykonawca, który nie zna `SPEC-0`, najpierw zapisuje własnymi słowami, czym jest aplikacja, kto jej używa i co powoduje finalne zatwierdzenie. Następnie folder wraca do pierwotnego autora. Autor dostaje finalny kod, własny `SPEC-0`, wszystkie 12 kart oraz interpretację ostatniego wykonawcy i ocenia zgodność bez poprawiania aplikacji.

Jeśli uczestników jest mniej niż 12, aplikacja wykonuje kolejne okrążenia po osobach niebędących jej autorem. Autor jest pomijany przy zmianach 2–12 i wraca dopiero do końcowej oceny.

## 3. Kto co widzi

### Runda 1

Autor dostaje:

- folder z pustymi `index.html`, `styles.css`, `app.js`;
- krótki, kompletny opis obecnego produktu (`SPEC-0`);
- pierwszą małą funkcję do dodania.

`SPEC-0` jest pokazany jako obraz obok UI, ale poza folderem i kontekstem agenta. Autor nie dostaje listy przyszłych zmian. W ciągu 8 minut tworzy minimalny szkielet potrzebny do uruchomienia aplikacji i wykonuje wyłącznie pierwszą małą funkcję.

Autor nie zna zmian 2–12. W ramach timera może użyć dowolnej liczby promptów w swojej sesji, ale nie może tworzyć osobnego pliku z opisem produktu ani kopiować całego `SPEC-0` do komentarza lub ukrytej treści aplikacji.

### Rundy 2–12

Uczestnik dostaje tylko:

- bieżący kod aplikacji;
- ostatnią publiczną odpowiedź agenta w osobnym polu obok chatu;
- jedną nową funkcję.

Nie widzi wcześniejszych promptów, reasoningów, pierwotnego `SPEC-0` ani przyszłych zmian. Dostaje całkowicie świeżą konwersację i może prowadzić ją dowolną liczbą promptów do końca timera. Odpowiedź poprzednika nie jest automatycznie przekazana agentowi; człowiek sam wybiera z niej kontekst do własnego promptu. Timer nie resetuje się po kolejnym prompcie.

Do następnej rundy przechodzi wyłącznie ostatnia odpowiedź agenta z tej sesji. Nie jest skracana, filtrowana ani ograniczana liczbą znaków.

## 4. Jak ma wyglądać dobre zadanie

Każde zadanie musi mieć:

1. **Znany, prosty rdzeń** — sens aplikacji da się wyjaśnić jednym zwykłym zdaniem.
2. **Jedną ważną granicę** — np. program coś proponuje, ale nie wykonuje; coś rezerwuje, ale nie zużywa; tworzy kopię, ale nie zmienia źródła.
3. **12 małych funkcji użytkowych** — widocznych po uruchomieniu, nie będących technicznymi pracami porządkowymi.
4. **Dwie wiarygodne interpretacje większości kart** — poprawną w kontekście produktu i kuszącą, prowadzącą do innego produktu.
5. **Jeden spójny poprawny finał** — wszystkie 12 zmian może współistnieć bez sprzeczności.
6. **Co najmniej jeden spójny błędny finał** — aplikacja nadal działa, ale zmienił się jej użytkownik, główny obiekt, źródło prawdy albo rodzaj skutków ubocznych.
7. **Profesjonalną wiarygodność** — humor może występować w fabule, danych, tekstach UI lub drobnym efekcie wizualnym, ale aplikacja nadal ma przypominać narzędzie, które sensownie mogłoby istnieć w profesjonalnym środowisku.

## 5. Jaki dryft jest wartościowy

Dryft ma zmieniać produkt, a nie tylko psuć implementację.

Dobre osie:

- sugestia → samodzielna decyzja;
- podgląd → mutacja;
- operacja tymczasowa → trwały workflow;
- kopia → zmiana źródła;
- narzędzie lokalne → integracja wykonująca akcje;
- pomoc dla jednego użytkownika → inny główny użytkownik;
- element pomocniczy → nowy główny obiekt aplikacji.

Przykład abstrakcyjny: aplikacja tylko rekomenduje wariant. Karta mówi „dodaj akceptację”. Poprawna funkcja tworzy dane do przekazania dalej; kusząca funkcja zapisuje decyzję, uruchamia proces i robi z aplikacji system workflow.

## 6. Rozmiar jednej zmiany

Pierwsza runda trwa 8 minut, ponieważ startuje od pustych plików. Rundy 2–12 trwają po 4 minuty. Timer jest jedynym limitem promptów: uczestnik może wysłać ich dowolnie wiele, ale czas nie zaczyna się od nowa. Jedna zmiana powinna:

- zwykle dać się wykonać jednym dobrym promptem, lecz pozwalać na doprecyzowanie lub naprawę w tej samej sesji;
- dotknąć zwykle 1–2 małych plików;
- dać widoczny wynik w uruchomionej aplikacji webowej;
- wymagać około 60–120 sekund pracy agenta;
- nie wymagać sieci, instalacji zależności, migracji ani przebudowy architektury;
- kończyć się szybkim automatycznym testem w przeglądarce.

Runda 12 również jest implementacyjna. Nie może być samym podsumowaniem ani prezentacją wyniku.

## 7. Czego nowy bank nie może powtórzyć

- Fabuła nie może zasłaniać tego, czym naprawdę jest aplikacja.
- Humor ma wynikać z sytuacji, przykładowych danych, komunikatów lub efektu wizualnego, nie z niezrozumiałego słownictwa domenowego.
- Humor nie może zmieniać zadania w zabawkę: interfejs, zachowanie, kod i sposób pracy mają pozostać profesjonalne.
- Główną pułapką nie może być parser, cache, format standardu, timezone, rounding ani egzotyczny model danych.
- Karta nie może wymagać odgadnięcia arbitralnej reguły znanej tylko prowadzącemu.
- Zmiany nie mogą sobie przeczyć.
- Zadanie nie może być serią niezależnych technicznych ticketów bez wspólnej osi dryftu.
- Poprawne rozwiązanie nie może zależeć od wiedzy o przyszłych kartach.
- Nie budujemy dwunastu różnych stosów technologicznych.

## 8. Założenia logistyczne

- Każda aplikacja ma osobny folder z trzema pustymi, już istniejącymi plikami: `index.html`, `styles.css`, `app.js`.
- Bez frameworka, bundlera, backendu, sieci i instalowania zależności podczas warsztatu.
- Poprawna oraz zdryfowana wersja każdego produktu muszą działać i różnić się znaczeniem w samej stronie. Zadanie nie może opierać się na pozorowaniu zewnętrznych integracji lub skutków.
- Podgląd aplikacji jest otwarty w przeglądarce i odświeża się po zmianie kodu.
- Agent może edytować wyłącznie trzy istniejące pliki. Harness blokuje tworzenie wszystkich nowych plików i katalogów, w tym `.md`, `.txt`, dodatkowych handoffów i dokumentacji.
- Hidden testy oraz materiały prowadzącego znajdują się poza folderem widocznym dla uczestnika i agenta.
- Pełnego `SPEC-0` nie wolno kopiować do komentarzy, stałych tekstowych, ukrytego DOM ani innych atrap dokumentacji w kodzie.
- Krótkie komentarze techniczne, dobre nazwy, struktura kodu i widoczne zachowanie UI są legalnym nośnikiem sensu produktu.
- `SPEC-0` dla autora ma zwykle 180–350 słów, 3–5 typów informacji i 6–10 współzależnych niezmienników. Trudność wynika z liczby rozróżnień, nie ze sztucznej długości; spec nie może redukować się bezstratnie do jednego hasła.
- Karta zmiany dla uczestnika to zwykle jedno zdanie.
- Każda runda ma świeżą konwersację agenta. W jej obrębie liczba promptów jest dowolna; ogranicza ją wyłącznie wspólny timer.
- Harness korzysta z Deep Agents Code w UI. W tle ustawia katalog roboczy na folder bieżącej aplikacji, a uczestnik widzi terminalowy przebieg pracy agenta.
- Po rundzie harness zachowuje ostatnią odpowiedź agenta bez limitu znaków i pokazuje ją następnej osobie w osobnym polu tylko do odczytu. Nie przekazuje jej automatycznie do nowej konwersacji i nie przekazuje wcześniejszych odpowiedzi ani promptów.
- Liczba promptów, czas pracy i długość ostatniej odpowiedzi są mierzone, ale nie ograniczane osobnymi limitami.
- UI wydaje kartę człowiekowi; nie wstrzykuje jej automatycznie do promptu.
- Hidden checker zapisuje dryft, lecz go nie naprawia. Blokuje tylko przyszły zakres, tworzenie niedozwolonych plików lub obejście harnessu.

## 9. Kryterium powodzenia banku

W pilocie bez dobrze utrwalonego kontekstu znaczący dryft powinien wystąpić w ponad połowie łańcuchów. Jednocześnie uczestnik mający czytelny sens zapisany w kodzie lub odzyskany z ostatniej odpowiedzi agenta powinien móc bez zgadywania zachować pierwotny produkt.

Jeżeli wszyscy dryfują niezależnie od jakości kontekstu, zadanie jest losowe. Jeżeli nikt nie dryfuje bez kontekstu, karta jest zbyt oczywista.

## 10. Aktualny etap

Powstało 12 projektów zawierających:

- pełny `SPEC-0` i założony rozwój aplikacji od pustych plików;
- 12 dokładnych kart uczestników;
- poprawną oraz kuszącą implementację każdej karty;
- przewidywany łańcuch odpowiedzi agenta i narastania dryftu;
- hidden probes oraz ocenę profili promptowania `N/R/C`.

Każdy projekt ma pełny `SPEC-0`, 12 kart, poprawne i kuszące interpretacje, przewidywane odpowiedzi oraz hidden probes. Nadal bez implementacji harnessu.

## Decyzja potrzebna teraz

Do akceptacji są konkretne łańcuchy z [banku](README.md). Założenia wspólne pozostają następujące:

- proste, natychmiast zrozumiałe produkty;
- dryft na poziomie sensu i skutków ubocznych;
- profesjonalne aplikacje z opcjonalnymi elementami humorystycznymi;
- statyczne vanilla HTML, CSS i JavaScript;
- tylko kod aplikacji i ostatnia odpowiedź agenta przechodzą między rundami;
- dowolna liczba promptów w ramach nieprzedłużanego timera;
- brak limitu znaków ostatniej odpowiedzi;
- zakaz tworzenia nowych plików i kopiowania pełnego `SPEC-0` do kodu;
- pierwsza runda 8 minut, kolejne małe zmiany po 4 minuty;
- najpierw ocena 12 łańcuchów, dopiero potem implementacja harnessu.
