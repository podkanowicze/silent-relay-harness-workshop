# Instrukcja dla LLM-a: lokalny fallback DeepAgents

Skopiować cały plik do LLM-a pracującego w firmowym środowisku.

## Zadanie

Zbuduj działający adapter DeepAgents do istniejącego `workshop-runner` oraz minimalny controller warsztatu.

Najpierw sprawdź repo, runtime i faktycznie zainstalowaną wersję DeepAgents. Nie wymyślaj API. Kod zależny od wersji zamknij w jednym adapterze.

## Niezmienniki

- Maks. 12 uczestników, 12 stacji i 12 rund.
- Agent uruchamia się lokalnie na DevPodzie bieżącego uczestnika.
- Każda tura dostaje świeży state agenta.
- Kontekst tury: prompt uczestnika + workspace; bez starych promptów i transcriptu.
- Stacja przenosi tylko dozwolone pliki aplikacji i ostatnią odpowiedź agenta.
- UI pokazuje bieżącą deltę, a w rundzie 1 także `SPEC-0`; nie dodaje ich automatycznie do kontekstu agenta.
- Przyszłe delty i wszystkie probes istnieją tylko na controllerze.
- Controller nie przechowuje ani nie przekazuje credentiali modelu.
- Dowolna liczba promptów w jednej świeżej sesji, ograniczona wyłącznie serwerowym timerem rundy.
- Delta 12 jest implementacyjna.
- Probes `SPEC-0`, required i regresje zapisują `PASS/DRIFT`; przyszły canary, chroniony obszar lub twardy skok zakresu blokuje jako `OVERSTEP`.
- Nie zapisuj ani nie pokazuj chain-of-thought.

## Dostarcz

1. lokalny terminalowy `workshop-runner`,
2. centralny controller bez dostępu do modelu,
3. panel administratora,
4. fake adapter do testów bez modelu,
5. runnable instrukcję uruchomienia.

## Adaptery

- `LocalAgentRuntimeAdapter` — invoke/cancel nowej sesji.
- `StationBundleAdapter` — fetch/publish bundle’a.
- `WorkspaceAdapter` — izolowany katalog rundy.
- `SnapshotAdapter` — hash, diff, restore.
- `IdentityAdapter` — uczestnik/admin bez tokenu modelu.
- `RotationPolicy` — macierz 12×12.
- `ClockAdapter` — czas serwerowy i fake clock.
- `CheckerAdapter` — checker per zadanie.
- `TurnMaterialAdapter` — wyłącznie tekst `Karta` bieżącej delty oraz `SPEC-0` tylko dla R1; bez `Oracle` i listowania przyszłych.
- `ScopeGateAdapter` — required, regression, future canaries i protected paths.
- `ProductIdentityAdapter` — zdanie autora w R1 i odgadnięcie produktu po R12.
- `ResultSinkAdapter` — eventy, ostatnie odpowiedzi agentów i wyniki.

Brakujące firmowe integracje zastąp fake adapterami i wskaż punkt podłączenia.

## Reguły transakcyjne

- Klucz: `workshop_id + station_id + round`.
- `turn_ticket` jest podpisany, jednorazowy i przypisany uczestnikowi.
- Runner wysyła propozycję; `PASS/DRIFT` publikuje przy oczekiwanym `base_version`, `OVERSTEP` odrzuca.
- Retry publikacji nie wywołuje agenta drugi raz.
- Timer i stan rundy są serwerowe.
- Timeout kończy lokalnego agenta; część może przejść jako `DRIFT`, lecz `OVERSTEP` zachowuje poprzedni snapshot.
- `DRIFT` publikuje bez ujawniania diagnozy do debriefu; `OVERSTEP` zachowuje poprzedni `base_version`. Kolejne prompty są możliwe tylko przed końcem bieżącego timera.
- Bundle nie zawiera credentiali, prompt history, reasoning ani session state.

## UI

Runner pokazuje: stację, rundę, timer, bieżącą deltę, ostatnią odpowiedź agenta, podgląd aplikacji, kod, pole promptu i status. Pole pozostaje dostępne do końca timera; każda wiadomość trafia do tej samej świeżej sesji rundy. W rundzie 1 UI pokazuje też `SPEC-0`. Materiały pozostają poza workspace, env, logiem i wiadomością agenta, chyba że człowiek przeniesie ich sens w prompt. Po R12 UI zbiera jednozdaniowe odgadnięcie produktu.

## Kryteria akceptacji

1. Controller działa bez jakiegokolwiek credentiala modelu.
2. Każda tura tworzy nowy agent state.
3. Fake model nie zna nonce poprzedniej tury, jeśli nie ma go w repo lub promptcie.
4. Dwa submit/publish nie tworzą dwóch tur.
5. Snapshot odtwarza identyczny hash.
6. Rotacja 12×12 nie powtarza stacji dla uczestnika.
7. Dwanaście runnerów działa równolegle bez mieszania bundle’i.
8. Timeout i reconnect nie resetują rundy.
9. Uczestnik nie pobierze cudzej stacji ani endpointu admina.
10. Eksport nie zawiera credentiali ani reasoning.
11. `zaimplementuj następną zmianę` nie powoduje pobrania delty przez agenta.
12. Implementacja niewydanej delty w rundach 1–11 daje `OVERSTEP` i nie zmienia snapshotu.
13. Każda niewydana delta ma co najmniej jeden behawioralny future canary.
14. `SPEC-0` jest wydawany tylko w R1; może wrócić później wyłącznie jako artefakt zapisany przez uczestnika.
15. Utrata niezmiennika `SPEC-0` publikuje się jako ukryty `DRIFT`, nie blokada.

## Rezultat

Dostarcz kod MVP, diagram, model danych, maszynę stanów, testy, instrukcję uruchomienia i listę firmowych punktów integracji. Nie kończ na pseudokodzie.
