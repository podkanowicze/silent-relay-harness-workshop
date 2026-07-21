# Decyzja: licencje kontra ciągłość sesji

## Nie da się mieć naraz

1. Copilot każdego uczestnika działa lokalnie na jego koncie.
2. Ta sama natywna sesja Copilota przechodzi między kontami.
3. Poprzednie prompty są technicznie niewidoczne na DevPodzie odbiorcy.

Stan sesji jest lokalny, a zdalne sterowanie Copilot CLI jest przypisane do konta, które uruchomiło sesję.

## Decyzja warsztatu

Zachowujemy `1 + 3`, rezygnujemy z `2`.

- Każda osoba uruchamia świeżą sesję własnego Copilota.
- Stacja przenosi kod aplikacji i ostatnią odpowiedź agenta.
- Poprzednie prompty, reasoning i session state nie są transferowane.
- To tworzy prawdziwy głuchy telefon i zwiększa dryft.

## Kontrola porównawcza

Jeżeli chcemy zmierzyć wpływ trwałej pamięci agenta, uruchamiamy osobny przebieg na zatwierdzonym DeepAgents. Nie nazywamy go przebiegiem indywidualnych licencji Copilot.

## Źródła

- [Uwierzytelnianie Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli)
- [Lokalny katalog danych i sesji](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference)
- [Remote control wymaga tego samego konta](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-remote-control)
