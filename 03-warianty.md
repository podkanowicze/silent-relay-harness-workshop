# Warianty

## S — rekomendowany

- Seed jest kompletnym produktem.
- Autor dostaje `SPEC-0 + DELTA-1`; przyszłych delt nie zna.
- Kolejni dostają tylko kod aplikacji, ostatnią odpowiedź agenta i bieżącą deltę.
- Pełny spec znika po rundzie 1. Nie wolno kopiować go do dokumentacji, długiego komentarza ani ukrytego UI.
- Każda delta ma poprawne rozwiązanie zgodne z `SPEC-0`, ale także kuszącą złą interpretację.
- Każda runda używa świeżej lokalnej sesji Copilota.

Testuje: czy sens produktu pozostaje czytelny w działającym kodzie i naturalnej odpowiedzi agenta, czy ginie po pierwszym człowieku.

## Kontrola — `SPEC-0` jawnie dostępny

- Uruchamiana tylko w osobnym pilocie, nie podczas właściwych 90 minut.
- Runner pokazuje `SPEC-0` każdej osobie poza workspace aplikacji.
- Różnica wyniku mierzy koszt utraty pierwotnego kontekstu.

## Kontrola techniczna — automatyczne wstrzyknięcie

- Runner dodaje `SPEC-0` i bieżącą deltę do każdego promptu.
- Eliminuje pracę człowieka nad kontekstem.
- Służy tylko do walidacji tasków i oracle.

## Antywzorzec — roadmapa 12 delt dla autora

Nie używać. Umożliwia zlecenie wszystkiego lub zapisanie pełnej kolejki zmian, więc usuwa eksperyment.

## Tryb kontrolny — trwały agent

- Jeden zaakceptowany backend zachowuje prywatny thread stacji.
- Testuje wpływ pamięci agenta, nie czysty głuchy telefon.
- Nie używa indywidualnych licencji Copilot uczestników.

Nie uruchamiać dwóch wariantów podczas jednych 90 minut.
