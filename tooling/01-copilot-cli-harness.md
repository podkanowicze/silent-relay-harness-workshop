# Lokalny runner Copilot CLI

## Zasada

Runner działa na DevPodzie uczestnika i korzysta z jego istniejącego logowania Copilot. Controller nigdy nie uruchamia Copilota.

Dokładnie jedną deltę wymuszają razem:

1. brak przyszłych delt na DevPodzie,
2. ogólna polityka agenta bez treści delt,
3. zewnętrzny scope gate przed publikacją.

Sama instrukcja „zrób tylko jedną zmianę” nie jest zabezpieczeniem.

Każda tura ma:

- świeży losowy UUID sesji,
- nowy katalog rundy,
- snapshot jednej stacji,
- bieżącą deltę widoczną tylko w UI runnera,
- w rundzie 1 także `SPEC-0`,
- dowolną liczbę promptów do końca timera,
- jedną przekazywaną dalej odpowiedź: ostatnią odpowiedź agenta z sesji.

Nie używać `--continue`, `--resume` ani UUID poprzedniej osoby.

## Kontrakt sesji

Transport Copilota musi utrzymywać jedną lokalną sesję przez czas rundy:

```text
open(turn_uuid, workspace, tool_allowlist) -> session
send(session, prompt) -> agent_response
send(session, next_prompt) -> agent_response
close(session) -> last_agent_response
```

Każdy `send` trafia do tej samej sesji bieżącego uczestnika. Liczba wywołań nie jest limitowana; runner odrzuca nowe wejście dopiero po końcu timera. `SPEC-0`, delta i ostatnia odpowiedź poprzednika nie są automatycznie doklejane do wiadomości modelu.

Jednorazowe wywołanie programmatic CLI przez zamknięty stdin nie wystarcza do tego kontraktu. Konkretny adapter wielowiadomościowy — interaktywny Copilot, SDK/ACP albo firmowy fallback — musi zostać potwierdzony w pilocie. Nie wolno emulować ciągłości przez przekazywanie sesji poprzedniej osoby.

Przypięty profil `.github/agents/workshop-turn.agent.md` zawiera wyłącznie ogólną politykę:

> Zaimplementuj wyłącznie jawnie opisany rezultat. Nie zgaduj roadmapy ani kolejnych funkcji. Po każdej wiadomości krótko opisz zmianę i test.

Profil nie zawiera `SPEC-0`, numeru delty, acceptance signal ani przyszłych wymagań. Jest warstwą sterującą, nie granicą bezpieczeństwa.

Nie dodawać `-p`: przy jednoczesnym `-p` Copilot ignoruje piped input. Nie umieszczać promptu w argv i nie uruchamiać procesu przez shell.

## Tura

1. Zweryfikuj podpis i jednorazowość `turn_ticket`.
2. Pobierz bundle i sprawdź hash `base_version`.
3. Rozpakuj do nowego katalogu ograniczonego do stacji.
4. Pokaż aplikację, kod, ostatnią odpowiedź agenta i deltę; w R1 także `SPEC-0` oraz zapieczętuj zdanie autora.
5. Utwórz świeży UUID i otwórz lokalną sesję Copilota; materiałów UI nie zapisuj automatycznie w workspace ani env.
6. Do końca timera przyjmuj kolejne prompty i przekazuj je do tej samej sesji.
7. Po każdym wywołaniu pokaż odpowiedź uczestnikowi; nie publikuj reasoning ani tool trace.
8. Po zamknięciu wejścia zachowaj wyłącznie ostatnią odpowiedź agenta, bez limitu znaków.
9. Utwórz propozycję snapshotu i diffstat.
10. Wyślij propozycję z oczekiwanym `base_version`.
11. Controller uruchamia ukryty scope gate.
12. Publikuj `PASS/DRIFT`; przy `OVERSTEP` zachowaj poprzedni snapshot i zamknij lokalną sesję.

„Zaimplementuj następną zmianę” nie uruchamia lookupu. `SPEC-0` nie jest roadmapą, a zgadniętą przyszłą deltę wykrywa canary.

## Timeout

- Timer pochodzi z controllera.
- Koniec czasu blokuje wejście, potem anuluje lokalny proces.
- Częściowy workspace staje się propozycją; przechodzi jako `PASS/DRIFT`, nie jako `OVERSTEP`.
- Retry sieci publikacji nie wywołuje modelu ponownie.
- Timer nie resetuje się po żadnym prompcie. Po blokadzie wejścia nie można otworzyć nowej sesji ani wysłać kolejnej wiadomości.

## Dane i tożsamość

- Copilot działa jako lokalnie zalogowany uczestnik.
- Token, auth store i `COPILOT_HOME` nie opuszczają DevPoda.
- Controller zapisuje `participant_id`, nie właściciela cudzej licencji.
- Prompt może trafić do prywatnego audytu dopiero po wykonaniu lokalnym.
- Bundle następnej rundy nie zawiera promptu ani katalogu sesji.
- `Oracle`, przyszłe delty i hidden probes nigdy nie opuszczają controllera.
- Workspace zawiera wyłącznie ustalone wcześniej pliki vanilla HTML/CSS/JS. Nowe pliki, dokumentacja i pełne kopie `SPEC-0` w komentarzu lub ukrytym DOM są odrzucane przez scope gate.

## Skala

Przy 12 osobach: 12 lokalnych sesji równolegle na rundę i 144 sesje łącznie. Liczba wiadomości zależy od uczestników i timera. Pilot sprawdza limity każdego konta oraz transfer małych bundle’i.

## Źródła

- [Programmatic CLI i stdin](https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/run-cli-programmatically)
- [Opcje CLI](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)
- [Custom agents w Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/invoke-custom-agents)
- [Hooks Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/hooks)
- [Uwierzytelnianie lokalne](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli)
