# Start na 12 DevPodach

## Rekomendacja

Wbudować `workshop-runner` do obrazu DevPoda. Na sali uczestnik wykonuje tylko `join`; nie dostaje pliku konfiguracyjnego.

## Dzień wcześniej

1. Wystawić controller prowadzącego pod firmowym HTTPS.
2. Przygotować 12 działających seedów, 12 speców, 144 delty i hidden gates.
3. Przypiąć wersję runnera, Copilot CLI, model i effort.
4. Sprawdzić lokalne logowanie Copilot każdego uczestnika.
5. Sprawdzić outbound DevPod → controller oraz DevPod → Copilot.
6. Przeprowadzić próbę transferu bundle’a w obie strony.

## Na sali

1. Prowadzący pokazuje URL i 12 jednorazowych kodów.
2. Każdy otwiera swój DevPod i uruchamia:

```text
workshop-runner join https://HOST/w/ID ONE_TIME_CODE
```

3. Runner lokalnie sprawdza `COPILOT_AUTH_OK`, wersję i wolne miejsce.
4. Do controllera wysyła tylko ID uczestnika, wersję runnera i status.
5. Dashboard pokazuje `12/12 READY`; prowadzący klika `START`.

Cel: 5 minut. Twardy limit: 8 minut.

## Każda runda

```text
controller
  → ticket + kod aplikacji + ostatnia odpowiedź + delta + opcjonalny SPEC-0 dla R1
  → lokalny runner
  → lokalny Copilot uczestnika
  → propozycja snapshotu + final answer
  → hidden scope gate
  → PASS/DRIFT: publikacja / OVERSTEP: poprzedni snapshot
  → controller
```

Prompt nie idzie przez controller przed wykonaniem. Przyszłe delty nie idą na DevPod. Token nigdy nie opuszcza DevPoda.

## Gdy runnera nie ma w obrazie

- Udostępnić jeden podpisany, przypięty artefakt z wewnętrznego registry.
- Pobrać i rozgrzać go przed dniem warsztatu.
- Nie instalować 12 różnych konfiguracji na początku zajęć.

## Plan awaryjny

| Problem | Decyzja po 2 minutach |
|---|---|
| Jeden lokalny Copilot bez auth | naprawa poza rundą albo `TIMEOUT` tej tury |
| Runner nie łączy się | HTTPS long-poll zamiast WSS |
| Transfer bundle’a pada | ponów idempotentnie; bez drugiego model call |
| Copilot pada w turze | lokalny DeepAgents albo gate częściowej propozycji |
| Więcej niż 8 minut startu | tryb zredukowany, bez dalszej konfiguracji |

## Czego nie robić

- Nie przesyłać promptu do Copilota na innym DevPodzie.
- Nie zbierać tokenów uczestników w controllerze.
- Nie kopiować `session-state` między kontami.
- Nie wznawiać sesji poprzednika.
- Nie dawać uczestnikowi ręcznie 12 repo i 12 konfiguracji.

## Oficjalne podstawy

- [Lokalne uwierzytelnianie Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli)
- [Programmatic CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/run-cli-programmatically)
- [Katalog lokalnych danych CLI](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference)
