# Lokalny Copilot SDK / ACP

To opcjonalna implementacja runnera. Runtime i token nadal pozostają na DevPodzie uczestnika.

## Topologia

```text
lokalny workshop-runner
  ├─ TUI rundy
  ├─ SDK: lokalny CopilotClient
  └─ ACP: copilot --acp po loopback
        ↓
lokalny workspace rundy

controller ↔ tylko kod aplikacji, ostatnia odpowiedź, snapshot i status
```

## Reguły

- Utwórz nową sesję dla każdej tury; nie wznawiaj sesji stacji.
- ACP słucha wyłącznie na loopback i kończy się po publikacji tury.
- SDK dostaje narzędzia ograniczone do katalogu rundy i dozwolonego testu.
- SDK dodaje do `systemMessage` tylko ogólną politykę jednej jawnej delty.
- UI renderuje deltę oraz, wyłącznie w rundzie 1, `SPEC-0`; nic nie trafia automatycznie do wiadomości systemowej.
- UI pozwala wysyłać kolejne wiadomości do tej samej sesji aż do końca timera; timer nie resetuje się.
- Token pobiera lokalny runtime; runner nie wysyła go controllerowi.
- `abort()` kończy lokalną pracę; częściowy workspace wysyłamy wyłącznie jako propozycję do gate.
- Participant UI pokazuje odpowiedź po każdym `session.idle`, a po zamknięciu rundy publikuje wyłącznie ostatnie `assistant.message`, bez limitu znaków.
- Odrzucaj przy ingest `assistant.reasoning*` i argumenty narzędzi.
- Snapshot jest propozycją; controller publikuje go dopiero po scope gate.

Polityka systemowa utrudnia nadmiarową implementację, ale jej nie dowodzi. Twardą granicą są nieobecne przyszłe delty oraz hidden future canaries na controllerze.

## Kiedy warto

- potrzebny pewny abort i streaming statusu,
- proces CLI na każdą turę startuje zbyt wolno,
- chcemy lokalny terminalowy skin bez natywnego timeline’u.

## Ryzyko

SDK i ACP są w public preview. Przypiąć kompatybilne wersje i mieć prosty fallback do programmatic CLI.

## Źródła

- [ACP server](https://docs.github.com/en/copilot/reference/copilot-cli-reference/acp-server)
- [Zdarzenia SDK](https://docs.github.com/en/copilot/how-tos/copilot-sdk/use-copilot-sdk/streaming-events)
- [Zgodność SDK–CLI](https://docs.github.com/en/copilot/how-tos/copilot-sdk/troubleshooting/compatibility)
- [System message SDK](https://github.com/github/copilot-sdk/blob/main/CHANGELOG.md)
