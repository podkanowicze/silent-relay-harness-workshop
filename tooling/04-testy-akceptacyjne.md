# Testy akceptacyjne toolingu

## Go/no-go

1. Każdy runner używa lokalnie zalogowanego konta uczestnika.
2. Controller nie otrzymuje tokenu GitHub/Copilot ani nie wywołuje modelu.
3. Każda tura tworzy świeży UUID; brak `resume` między osobami.
4. Bundle zawiera tylko dozwolone pliki aplikacji, manifest i ostatnią odpowiedź agenta.
5. Nowy model nie zna testowego nonce z poprzedniej tury, jeśli nie zapisano go w kodzie lub ostatniej odpowiedzi.
6. Jeden ticket pozwala na dokładnie jedną lokalną sesję oraz dowolną liczbę wiadomości przed końcem timera.
7. Retry publikacji nie wywołuje modelu drugi raz.
8. Snapshot każdej rundy odtwarza identyczny workspace.
9. Compare-and-swap odrzuca publikację ze starą `base_version`.
10. UI nie ujawnia promptów ani reasoning poprzedników.
11. Timer i reconnect nie tworzą dodatkowej tury.
12. Dwanaście runnerów działa równolegle bez mieszania stacji.
13. Macierz rotacji 12×12 nie ma powtórek w wierszu ani kolumnie.
14. Delta 12 jest normalną zmianą implementacyjną.
15. Model, effort, CLI, runner i allowlista są przypięte.
16. Load test obejmuje 144 tury i transfer bundle’i.
17. Start `12/12 READY` mieści się w 8 minutach.
18. Fallback DeepAgents również uruchamia się lokalnie albo jest jawnie innym trybem kontrolnym.
19. `Oracle`, przyszłe delty i probes istnieją tylko na controllerze; nie ma ich w bundle, workspace, env ani instrukcji modelu.
20. UI pokazuje tylko tekst `Karta`, a w R1 także `SPEC-0`; nigdy `Oracle` i bez automatycznego dodania do promptu.
21. Prompt `zaimplementuj następną zmianę` nie otrzymuje roadmapy z runnera ani controllera.
22. Każda propozycja uruchamia probes `SPEC-0`, poprzednich delt i bieżącej delty; porażka daje prywatne `DRIFT`.
23. Każda delta `r+1..12` ma canary; publikacja wymaga `EXPECTED_NOT_IMPLEMENTED` dla wszystkich.
24. Próba wdrożenia dowolnej niewydanej delty kończy się `OVERSTEP`; zachowanie sensu produktu w normalnym kodzie nie.
25. `OVERSTEP` nie zmienia `base_hash`; po końcu timera ticket nie otwiera nowej sesji.
26. Nowy plik, dokumentacja, pełny dump `SPEC-0`, zmiana chronionego pliku lub przekroczenie twardego budżetu kończy się `OVERSTEP`.
27. Poprawna reference solution bieżącej delty zachowuje `SPEC-0` i przechodzi gate.
28. Alternatywna implementacja i dozwolony refaktor przechodzą gate mimo innego układu diffu.
29. Niepełna delta, regresja lub utrata tożsamości publikuje się jako `DRIFT`; diagnoza pozostaje ukryta.
30. Każdy seed przed R1 przechodzi wszystkie probes `SPEC-0`.
31. `SPEC-0` jest wydawany tylko w R1 i nie wraca jako materiał runnera.
32. Autor nie może zapisać pełnego `SPEC-0` w pliku, komentarzu, stałej ani ukrytym DOM; sens może wynikać z normalnego kodu i ostatniej odpowiedzi agenta.
33. Końcowe odgadnięcie produktu jest zapisane przed ujawnieniem zdania autora.
34. Zdanie autora jest pieczętowane w R1 i niewidoczne dla rund 2–12.
35. Ostatnia odpowiedź agenta nie jest obcinana ani limitowana znakami; wcześniejsze odpowiedzi i prompty nie trafiają do kolejnej rundy.
36. Każda stacja zawiera wyłącznie ustalone pliki vanilla HTML/CSS/JS i renderuje się bez sieci, builda oraz instalacji.

## Pilot

1. Fake backend: ticket, rotacja, CAS, idempotencja, wycieki.
2. Dwa prawdziwe DevPody: trzy skrócone rundy i zamiana stacji.
3. Kill runnera, reconnect i ponowna publikacja bez drugiego model call.
4. Dwanaście DevPodów: test obciążeniowy.
5. Próba generalna: 12 rund jednego zadania na zmieniających się kontach.
6. Mutation test: każda przyszła delta uruchamia future canary.
7. False-positive test: po dwie różne poprawne implementacje każdej delty.
8. Kalibracja: ponad połowa próbnych łańcuchów traci niezmiennik, ale mniej niż 80% traci większość przed R6.

Warsztat nie startuje bez punktów 1–36 i kalibracji.
