# Scope gate: dokładnie jedna delta

## Decyzja

Twarde wymuszenie działa, bo każdy dostaje tylko bieżącą deltę. Przyszłe delty i ich testy istnieją wyłącznie na controllerze.

Autor dostaje pełny `SPEC-0`, lecz seed już go spełnia. Spec opisuje sens produktu, nie roadmapę 12 przyszłych zmian.

## Rozdział danych

| Dane | Człowiek | Lokalny Copilot | Controller |
|---|---:|---:|---:|
| Kod aplikacji + ostatnia odpowiedź | tak | kod przez workspace; odpowiedź tylko jeśli przeniesie ją człowiek | tak |
| `SPEC-0` | tylko autor w R1 | tylko jeśli przeniesie go autor | tak |
| Tekst `Karta` bieżącej delty | UI, tak | tylko jeśli opisze go człowiek | tak |
| `Oracle` bieżącej delty | nie | nie | tak |
| Przyszłe delty | nie | nie | tak |
| Probes i oczekiwane wyniki | nie | nie | tak |

Materiały UI nie trafiają automatycznie do pliku, env, custom instruction ani prefiksu promptu. Bundle nie zawiera roadmapy ani nazw przyszłych testów. Workspace ma zamkniętą listę istniejących plików aplikacji i nie dopuszcza osobnej dokumentacji.

## Tura

1. Controller wydaje ticket: `task`, `round`, `base_hash`, `gate_id`, budżet zmian.
2. UI pokazuje bieżącą deltę; w rundzie 1 także `SPEC-0`.
3. Runner otwiera snapshot i uruchamia Copilota ze świeżym UUID.
4. Do modelu trafiają wyłącznie prompty bieżącej osoby oraz workspace; liczba promptów jest dowolna do końca timera.
5. Runner wysyła snapshot i diff do controllera.
6. Controller sprawdza snapshot w izolowanym checkerze.
7. `PASS` lub `DRIFT` publikuje snapshot; tylko `OVERSTEP` zachowuje `base_hash`.

Prompt „zaimplementuj następną zmianę” nie ma ukrytej roadmapy. Może co najwyżej zgadywać z repo i wytworzyć mierzony `DRIFT`.

## Gate rundy `r`

```text
AUDIT: spec0_invariant_probes -> PASS | IDENTITY_DRIFT
AUDIT: prior_delta_probes     -> PASS | DRIFT
AUDIT: required_probe[r]      -> PASS | DRIFT
BLOCK: future_canaries[r+1..12] == EXPECTED_NOT_IMPLEMENTED
BLOCK: protected_paths     == UNCHANGED
BLOCK: new_files           == NONE
BLOCK: spec_dump           == NONE
BLOCK: hard_change_budget  == OK
```

- `spec0_invariant_probes`: mierzą, czy aplikacja nadal jest produktem autora; nigdy nie blokują publikacji.
- `required_probe`: obserwowalny rezultat bieżącej delty; mierzy wykonanie, nie prostuje eksperymentu.
- `future-canary probes`: co najmniej jeden sygnał dla każdej niewydanej delty; wszystkie mają pozostać nieobecne.
- `protected_paths`: manifest, checker, instrukcje i dane rund.
- `hard_change_budget`: tylko oczywisty skok zakresu, np. zależność, chroniony obszar albo wielokrotność normalnego diffu.

Nowy plik, osobna dokumentacja albo pełny `SPEC-0` skopiowany do komentarza, stałej tekstowej lub ukrytego DOM jest `OVERSTEP`. Krótkie komentarze techniczne, nazwy i normalna treść widocznego UI pozostają dozwolone.

Implementacja dowolnej przyszłej delty musi uruchomić canary. Samo zachowanie kompletnego `SPEC-0` nigdy nie jest `OVERSTEP`.

## Wynik

- `PASS`: delta, wcześniejsze kontrakty i `SPEC-0` przechodzą; publikacja.
- `DRIFT`: brak delty, regresja lub utrata tożsamości, ale bez przyszłego zakresu; publikacja i prywatna adnotacja.
- `OVERSTEP`: przyszły canary przeszedł, zmieniono chroniony obszar albo przekroczono twardy limit; brak publikacji.

Przy `OVERSTEP` controller nie publikuje snapshotu. Stacja pozostaje na `base_hash`; katalog rundy jest usuwany lub zachowany wyłącznie w prywatnym audycie. W trakcie aktywnego timera uczestnik może poprawiać workspace kolejnymi promptami, lecz po zamknięciu rundy ticket nie uruchamia nowej sesji.

`DRIFT` nie ujawnia wyniku hidden probes w trakcie gry. Przy `OVERSTEP` następna osoba dostaje komunikat `PROPOZYCJA ODRZUCONA — KOD BEZ ZMIAN`, aby ostatnia odpowiedź modelu nie udawała opublikowanego stanu.

## Ograniczanie fałszywych alarmów

- Canaries badają publiczne zachowanie, nie nazwy plików ani konkretną implementację.
- Wspólny probe może pokrywać kilka delt, ale żadna przyszła delta nie może zostać bez sygnału.
- Nie blokują refaktoru, który tylko przygotowuje kod pod przyszłość.
- Miękki budżet daje adnotację, nie automatyczne `OVERSTEP`.
- Twarde limity dotyczą tylko oczywistego skoku zakresu i chronionych danych.
- Reference solution bieżącej delty musi zachować `SPEC-0` i przejść gate.
- Reference solution zawierające delty `r+1..12` musi zostać odrzucone w rundach 1–11.
- Autor zadania sprawdza canaries także na dwóch alternatywnych poprawnych implementacjach.
- Cały gate jednej stacji ma kończyć się w kilka sekund.

Scope gate nie dowodzi matematycznie, że wykonano tylko jedną deltę. Egzekwuje górną granicę zakresu, ale celowo przepuszcza zmianę sensu produktu, żeby mogła zostać ujawniona na końcu.
