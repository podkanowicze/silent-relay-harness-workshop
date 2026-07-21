# ARCHIVE — odrzucony projekt Copilot/ACP

Ten katalog opisuje wcześniejszy wariant i nie jest instrukcją dla bieżącej aplikacji. Aktualny runner oraz uruchomienie: [Context Telephone application](../WORKSHOP-APP.md).

## Twardy warunek

- Copilot, konto i licencja zostają na DevPodzie uczestnika.
- Controller nie dostaje tokenu i nie wywołuje modelu.
- Nie przenosimy sesji Copilota między osobami.
- Między DevPodami krążą tylko dozwolone pliki aplikacji i ostatnia odpowiedź agenta.

## Decyzja

| Priorytet | Wariant | Start uczestnika |
|---:|---|---|
| 1 | Runner w obrazie DevPoda | jedna komenda `join` |
| 2 | Przypięty runner z wewnętrznego artefaktu | pobranie + `join` |
| 3 | Lokalny adapter DeepAgents | ten sam runner |

## Niezmiennik

```text
uczestnik = własny DevPod + własne konto + lokalny Copilot
stacja = spec_id + wersja repo + ostatnia odpowiedź
tura = uczestnik + stacja + świeży UUID sesji
```

## Topologia

```text
controller prowadzącego
  ├─ timer, rotacja, turn tickets
  ├─ 12 snapshotów kodu aplikacji
  ├─ 12 × SPEC-0 + 144 delty + hidden gates
  ├─ ostatnie odpowiedzi agentów
  └─ checker + audit
          ↕ outbound HTTPS
12 × lokalny workshop-runner
          ↓
12 × lokalny Copilot CLI / DeepAgents
```

## Przebieg tury

1. Runner pobiera ticket, snapshot kodu, ostatnią odpowiedź i bieżącą deltę.
2. UI pokazuje aplikację, kod, ostatnią odpowiedź i deltę; w rundzie 1 także `SPEC-0`.
3. Runner tworzy świeży UUID i uruchamia lokalnego Copilota.
4. Uczestnik wysyła dowolną liczbę promptów do końca wspólnego timera.
5. Copilot zmienia wyłącznie istniejące pliki aplikacji dopuszczone manifestem.
6. Runner wysyła propozycję snapshotu oraz ostatnią, nieobciętą odpowiedź agenta.
7. Controller uruchamia gate: `PASS/DRIFT` publikuje, `OVERSTEP` odrzuca.

Controller może zapisać prompt dopiero jako wynik audytowy. Nie wysyła go do modelu.

## Wspólny kontrakt

```text
join(participant_id, pair_code) -> runner_ticket
assignment(runner_ticket, round) -> turn_ticket
fetch_station(turn_ticket) -> base_version + app_bundle + last_agent_response
fetch_turn_materials(turn_ticket) -> current_delta_card + optional_spec0
seal_founder_identity(turn_ticket, one_sentence) -> sealed
propose_turn(turn_ticket, base_version, snapshot, last_agent_response, audit_prompts) -> gate_result
submit_product_guess(turn_ticket, one_sentence) -> sealed
health(runner_ticket)
```

Publikacja po `PASS/DRIFT` używa compare-and-swap na `base_version`. Token GitHub/Copilot nie jest polem żadnego kontraktu.
`turn_ticket` działa tylko dla przypisanej stacji i rundy; API nie listuje ani nie pobiera przyszłych delt.

## Granice

- Bundle nie zawiera promptów, transcriptu, reasoning ani `session-state`.
- `SPEC-0` jest dostępny w UI tylko w rundzie 1; autor może świadomie utrwalić go przez prompt.
- Bieżąca delta jest warstwą UI; nie trafia automatycznie do workspace, env ani promptu modelu.
- `Oracle` bieżącej delty pozostaje na controllerze razem z probes.
- Przyszłe delty i probes nie opuszczają controllera.
- Świeża sesja nie dostaje automatycznie ostatniej odpowiedzi poprzedniego agenta; przekłada ją człowiek.
- Uczestnik ma shell do własnego DevPoda, ale nie ma danych sesji poprzednika.
- Adapter musi utrzymywać wielowiadomościową sesję wyłącznie przez czas jednej rundy i zamknąć ją przed rotacją.
- Runner blokuje tworzenie nowych plików, dokumentacji i pełnych kopii `SPEC-0` w komentarzach lub ukrytym DOM.
- Model, effort, CLI i instrukcja harnessu są przypięte.

## Pliki

- [Start na 12 DevPodach](05-start-na-devpodach.md)
- [Lokalny runner Copilot CLI](01-copilot-cli-harness.md)
- [Lokalny wariant SDK / ACP](02-copilot-sdk-acp.md)
- [Instrukcja budowy fallbacku DeepAgents](03-deepagents-build-spec.md)
- [Testy akceptacyjne](04-testy-akceptacyjne.md)
- [Scope gate: dokładnie jedna delta](06-scope-gate.md)
- [Anty-skrót: model zagrożeń](07-anty-skrot.md)

## Oficjalne podstawy

- [Uwierzytelnianie Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli)
- [Programmatic Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/run-cli-programmatically)
- [Lokalne dane sesji](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference)
- [Custom agents](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/invoke-custom-agents)
- [Hooks](https://docs.github.com/en/copilot/concepts/agents/hooks)
