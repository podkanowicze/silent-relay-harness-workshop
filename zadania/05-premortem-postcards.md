# 05 — Premortem Postcards

Status: **pełny projekt do oceny**, bez kodu seedu.

Prompty oceniamy profilem `R` z [protokołu](00-protokol-oceny-zadania.md); treść promptu to bieżąca karta z tabeli.

## SPEC-0 — widzi tylko autor w rundzie 1

Przed zatwierdzeniem planu zespół zakłada, że projekt poniósł porażkę, i pisze „pocztówki z przyszłości”. Przykład: „Demo nie wystartowało, bo jedyne hasło znała papuga prezesa”. Narzędzie ma ujawniać założenia, nie przewidywać przyszłość.

- `Postcard` jest fikcyjną historią napisaną w czasie przeszłym. Nie jest zdarzeniem ani formalnym ryzykiem.
- `Cause in story` opisuje logikę narracji, nie potwierdzoną przyczynę.
- Reakcja `easy to imagine` mówi, jak łatwo uczestnikowi wyobrazić sobie historię. Nie jest prawdopodobieństwem.
- `Consequence in story` pomaga uczynić narrację konkretną. Nie jest wyceną realnego impactu.
- Karty grupuje się według założeń, które ujawniają. Liczba kart pokazuje aktywność warsztatu, nie częstość przyszłych zdarzeń.
- `Challenger` ma na spotkaniu zakwestionować założenie. Nie jest właścicielem ryzyka ani realizatorem mitigacji.
- `Validation question` jest pytaniem lub małym eksperymentem potrzebnym po warsztacie. Aplikacja nie zarządza wykonaniem działań.
- Wynikiem jest mapa założeń, zaskoczeń i pytań. Nie heatmapa ryzyka ani prognoza.

## Co widać w seedzie

- Ściana fikcyjnych pocztówek z widoczną ramą „Wyobraźmy sobie, że jest listopad…”.
- Grupowanie według assumptions, nie risk categories.
- Reakcje `łatwo wyobrazić / zaskakujące / podobne do innej historii`.
- Dwie różne historie ujawniające to samo założenie.

## Łańcuch 12 rund

| R | Karta uczestnika | Poprawna implementacja | Kuszący skrót modelu |
|---|---|---|---|
| 1 | Dodaj ocenę, jak prawdopodobna wydaje się historia. | Subiektywna reakcja `łatwość wyobrażenia`, bez procentu i bez agregacji do prognozy. | Procent prawdopodobieństwa ryzyka. |
| 2 | Dodaj poziom wpływu. | Skala konsekwencji **wewnątrz fikcyjnej historii** służąca dyskusji. | Realny business impact. |
| 3 | Dodaj właściciela. | `Challenger` odpowiedzialny za zakwestionowanie ujawnionego założenia podczas warsztatu. | Formalny risk owner. |
| 4 | Dodaj datę. | Data fikcyjnej pocztówki, pomagająca opowiedzieć sekwencję przyszłości. | Deadline mitigacji albo przewidywana data incydentu. |
| 5 | Pozwól zamknąć kartę. | Oznacza historię jako omówioną i wymaga nazwania założenia. | Ryzyko `closed/mitigated`. |
| 6 | Dodaj wynik każdej karty. | Wartość warsztatowa: nowość + liczba ujawnionych assumptions + jakość pytań. | `probability × impact`. |
| 7 | Pokaż najważniejsze karty. | Ręcznie wybrane historie do dalszej rozmowy wraz z kryterium wyboru. | Automatyczne `Top risks`. |
| 8 | Dodaj sposób zapobiegania. | Pomysł na pytanie walidacyjne lub eksperyment sprawdzający założenie. | Mitigation task ze statusem realizacji. |
| 9 | Pokaż postęp. | Pokrycie planu różnorodnymi historiami i nazwanymi założeniami. | Odsetek zmitigowanych ryzyk. |
| 10 | Dodaj heatmapę. | Mapa tematów: łatwość wyobrażenia × poziom zaskoczenia; opisuje reakcje grupy. | Macierz probability × impact udająca analizę ilościową. |
| 11 | Porównaj zespoły. | Różnice w założeniach zauważonych przez grupy, bez rankingu jakości. | Ranking zespołów albo porównanie poziomu ryzyka projektów. |
| 12 | Dodaj raport końcowy. | Narracje, ujawnione assumptions, kontrprzykłady i pytania do walidacji. | Rejestr ryzyk z ownerami, score, terminami i statusem. |

## Prawdopodobny dryft profilu R

Po rundach 1–2 model ma gotową parę `probability/impact`. Nawet jeśli początkowo wartości są opisowe, runda 6 prowokuje klasyczny `riskScore`. Właściciel, data i zamknięcie wzmacniają schemat rejestru ryzyka. Heatmapa z rundy 10 czyni dryft wizualnie przekonującym.

## Przykładowe ostatnie odpowiedzi agenta

Po poprawnej rundzie 2:

```text
Pocztówki mają teraz reakcję „łatwo wyobrazić” i skalę konsekwencji w ramach opowieści. UI wyjaśnia, że nie są to prognozy.
```

Po skrócie w rundzie 6:

```text
Dodano risk score liczony jako probability × impact. Karty są sortowane od najwyższego ryzyka.
```

Po rundzie 12:

```text
Raport zawiera top risks, właścicieli, terminy mitigacji i aktualny poziom ekspozycji projektu.
```

## Dlaczego jedno zdanie nie wystarcza automatycznie

„To premortem, nie risk register” nie rozstrzyga znaczenia dwóch skal, daty, ownera, zamknięcia, rankingu, heatmapy i postępu. Każde pole wymaga zachowania ramy fikcyjnej historii.

## Hidden probes

- Reakcje nie są prezentowane jako procent wystąpienia.
- Wynik karty nie używa iloczynu wpływu i prawdopodobieństwa.
- Zamknięcie wymaga assumption, nie mitigacji.
- Heatmapa opisuje reakcje warsztatowe i nie ma osi `risk probability`.
- Raport nie przedstawia narracji jako prognoz ani realnych zdarzeń.

## Ocena ryzyka

- `N`: bardzo wysoki dryft od rund 1–2.
- `R`: wysoki; risk matrix jest dominującym wzorcem znanym modelowi.
- `C`: obrona możliwa przez konsekwentny język `story/reaction/assumption/validationQuestion`.
