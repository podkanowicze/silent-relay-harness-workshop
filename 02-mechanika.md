# Mechanika

## Pięć warstw

- `SPEC-0`: pełna tożsamość i niezmienniki produktu; tylko autor w rundzie 1.
- `DELTA-R`: mała zmiana bieżącej rundy; tylko bieżący człowiek.
- Model: prompty bieżącego człowieka i kod aplikacji.
- Stacja: kod aplikacji oraz ostatnia odpowiedź agenta.
- Prowadzący: `SPEC-0`, 12 delt i końcowe oracle.

## Granica informacji

- Seed jest działającą aplikacją zgodną z `SPEC-0`.
- Runda 1 pokazuje autorowi `SPEC-0 + DELTA-1`.
- Od rundy 2 UI pokazuje tylko `DELTA-R`; pełny spec nie wraca.
- Autor może przekazać sens przez strukturę i nazewnictwo kodu albo naturalną odpowiedź agenta, ale nie może tworzyć dokumentacji ani kopiować pełnego `SPEC-0` do komentarzy lub ukrytego UI.
- Delta `R+1` jest wydawana dopiero po zamknięciu rundy `R`.
- Bieżące materiały widzi człowiek; runner nie dokleja ich automatycznie do promptu.
- Przyszłych delt nie ma w seedzie, repo, testach, nazwach ani instrukcji modelu.

## Jedna runda

1. Uczestnik pobiera przydzieloną stację.
2. Widzi repo, ostatnią odpowiedź i bieżącą deltę; w rundzie 1 także `SPEC-0`.
3. Łączy zmianę z odzyskanym sensem produktu; timer pokazuje tempo rundy.
4. Runner tworzy świeżą lokalną sesję Copilota.
5. Model dostaje wyłącznie kolejne prompty tej osoby i kod aplikacji.
6. Agent wykonuje zmianę; uczestnik może wysyłać następne prompty także po `00:00`, dopóki prowadzący nie zarządzi rotacji.
7. Runner wysyła propozycję snapshotu, diff, audit promptów i ostatnią odpowiedź agenta.
8. Controller mierzy niezmienniki `SPEC-0`, bieżącą deltę i future canaries.
9. `PASS` i ukryty `DRIFT` publikują snapshot; `OVERSTEP` przekazuje komunikat `KOD BEZ ZMIAN`.

## Reguły

- Jeden uczestnik, jedna świeża sesja, jeden informacyjny timer i jedna mała delta; liczba promptów w sesji jest dowolna.
- Wszystkie 12 delt jest implementacyjnych; baseline jest kompletny przed rundą 1.
- Agent jest jedynym wykonawcą zmian.
- Brak rozmów między uczestnikami.
- Między rundami legalną pamięcią są wyłącznie dozwolone pliki aplikacji oraz ostatnia odpowiedź agenta. Osobne handoffy i dokumentacja są zabronione.
- Ostatnia odpowiedź agenta nie ma limitu znaków i nie jest skracana.
- Workspace ma zamkniętą listę istniejących plików vanilla HTML/CSS/JS; agent nie może tworzyć nowych.
- Przyszłe delty nie są dostępne żadnemu uczestnikowi.
- Instrukcja systemowa zawiera tylko ogólną politykę zakresu; nigdy kartę ani plan zadania.
- „Zaimplementuj kolejną zmianę” nie ujawnia agentowi delty. Agent może jedynie zgadywać.
- Utrata niezmiennika `SPEC-0` jest mierzonym dryftem, nie blokadą.
- Pytanie, błąd lub timeout agenta staje się statusem rundy.
- `3:25`: blokada wejścia; `3:50`: abort; tylko przyszły zakres lub naruszenie harnessu blokuje workspace.

## Licencja i stacja

- Każdy uruchamia Copilota na swoim DevPodzie i swoim koncie.
- Controller nie dostaje tokenu i nie wywołuje modelu.
- Nie kopiujemy ani nie wznawiamy sesji Copilota między kontami.
- Stacja zachowuje kod aplikacji i ostatnią odpowiedź agenta, nigdy cudzą sesję, prompty lub historię shella.

## Rotacja

- Przy 12 osobach: co rundę jedna stacja dalej.
- Przydział: `stacja = 1 + ((uczestnik + runda - 2) mod 12)`.
- Po 12 rundach każdy odwiedza każdą stację dokładnie raz.

## Co zachowuje controller

1. snapshot i diff stacji,
2. ostatnią publiczną odpowiedź,
3. audit promptów i rund,
4. `SPEC-0`, 12 delt i hidden probes,
5. jednozdaniową tożsamość autora oraz końcowe odgadnięcie produktu.

Snapshot po każdej rundzie pozwala wskazać pierwszą utratę sensu. Sesja modelu nie jest częścią przekazywanego stanu.
