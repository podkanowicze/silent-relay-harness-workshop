# Protokół oceny zadania przed budową seedu

## Co musi być ocenialne

Sam pitch nie wystarcza. Dla każdego zadania trzeba zobaczyć:

1. pełny `SPEC-0` przekazany autorowi;
2. elementy produktu widoczne w początkowym UI i kodzie;
3. dokładne karty `DELTA-1…12`;
4. poprawną i kuszącą implementację każdej karty;
5. prawdopodobny kierunek odpowiedzi agenta;
6. moment, w którym lokalny skrót zmienia tożsamość aplikacji;
7. test rozróżniający poprawny finał od sprawnego technicznie dryftu.

## Prompty używane do oceny

Nie zakładamy limitu promptów. Timer trwa cały czas.

### Profil N — naiwny

```text
Zaimplementuj: <treść karty>.
```

### Profil R — rozsądny developer

```text
Przejrzyj istniejącą aplikację i ostatnie podsumowanie agenta.
Zaimplementuj: <treść karty>.
Zachowaj istniejące działanie i styl. Sprawdź rezultat.
```

### Profil C — context engineer

```text
Najpierw odtwórz z kodu, UI i poprzedniego podsumowania:
- użytkownika aplikacji,
- znaczenie głównych obiektów i statusów,
- granice odpowiedzialności.
Następnie zaimplementuj: <treść karty>.
Na końcu pozostaw następnej osobie krótkie podsumowanie produktu,
chronionych reguł i wykonanej zmiany.
```

Profil `R` jest główną kalibracją. `N` powinien dryfować częściej. `C` powinien móc obronić produkt — inaczej zadanie jest losową pułapką, a nie ćwiczeniem z context engineeringu.

## Co zwykle odpowie agent

Standardowa odpowiedź po implementacji opisuje diff:

```text
Dodano właściciela kart, filtrowanie po właścicielu i odpowiednie badge.
Zaktualizowano przykładowe dane oraz style. Aplikacja działa bez błędów.
```

Nie należy zakładać, że agent sam powtórzy pełny model produktu. Jeżeli uczestnik świadomie wymusi dobry handoff, jest to poprawne rozwiązanie ćwiczenia, nie obejście.

## Skąd ma wynikać trudność

Nie z limitu znaków. Każdy `SPEC-0` powinien zawierać minimum:

- 3–5 typów informacji o odmiennym znaczeniu;
- 5–7 współzależnych niezmienników;
- przynajmniej 4 terminy mające kuszące znaczenie w sąsiednim produkcie;
- regułę agregacji lub przejścia stanu, której nie widać z jednego ekranu;
- poprawne zachowanie, które wygląda mniej standardowo niż błędny wzorzec znany modelowi.

Jedno zdanie „to nie jest Jira” może zatrzymać część dryftu. Nie powinno jednak wystarczyć do poprawnego rozstrzygnięcia wszystkich późniejszych kart: `owner`, `priority`, `done`, `progress`, `overdue` i `summary` muszą odwoływać się do różnych reguł domenowych.

## Kiedy zadanie jest uczciwe

- Zła implementacja jest lokalnie rozsądna i dobrze wygląda.
- Poprawna implementacja wynika z `SPEC-0` oraz sygnałów, które dało się utrwalić w kodzie i UI.
- Karta nie zawiera sprzeczności z `SPEC-0`.
- Dryft zachodzi bez backendu i bez udawania skutków zewnętrznych.
- Hidden probe obserwuje zachowanie, nie nazwę zmiennej ani słowo kluczowe.
- Po dobrym handoffie profil `C` nie musi zgadywać.

## Kryterium pilota

Dla każdego zadania uruchomić minimum trzy łańcuchy:

- `N`: oczekiwany znaczący dryft;
- `R`: dryft w części łańcuchów, nie zawsze w tej samej rundzie;
- `C`: przeważnie zachowana tożsamość.

Zadanie odrzucamy, jeśli:

- `N` zawsze zachowuje produkt — za łatwe;
- `C` regularnie dryfuje — za mało odtwarzalnego kontekstu;
- jedna oczywista etykieta rozwiązuje wszystkie 12 kart;
- wynik zależy głównie od przypadku albo znajomości przyszłych delt.
