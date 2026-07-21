# Warsztat: context engineering przez „głuchy telefon”

Browser-based context-engineering workshop runner for 2–12 participants. Each
turn starts a fresh Deep Agents Code session and passes only the application
files plus the previous public reply to the next participant.

## Run it

See [INSTALL.md](INSTALL.md) for Linux/DevPod and Windows setup. The complete
runtime configuration and safety model are documented in
[WORKSHOP-APP.md](WORKSHOP-APP.md).

The two workshop entry points are:

- `/` — participant lobby and workspace,
- `/admin` — protected moderator controls and manual start.

Current review set: [Exercise Bank V2 — grounded product concepts](exercises-en-v2/README.md). The previous English set was rejected and is retained only as an archive.

Status: powstało 12 projektów zadań i działający runner przeglądarkowy. Instrukcja uruchomienia: [Context Telephone — application](WORKSHOP-APP.md).

## Teza

Warsztat rozdziela:

1. `SPEC-0`: kompletny sens działającego produktu,
2. `DELTA-R`: małą zmianę bieżącej rundy,
3. sesję uczestnika z informacyjnym timerem,
4. kod aplikacji i ostatnią odpowiedź agenta.

## Co ma zostać po warsztacie

- Pełna specyfikacja nie jest tym samym co trwały kontekst.
- W tym eksperymencie kontekst musi przeżyć w działającym kodzie albo ostatniej odpowiedzi agenta.
- Mała funkcja może zmienić sens całego produktu.
- Utracony niezmiennik kosztuje w każdej kolejnej turze.

## Rekomendowany format: SPEC-0 + 12 delt

- 90 minut; 12 osób, 12 stacji, 12 rund.
- Każda stacja zaczyna z małą, działającą i kompletną aplikacją vanilla HTML/CSS/JS.
- Autor w rundzie 1 dostaje pełny `SPEC-0` oraz małą kartę `DELTA-1`.
- Autor nie zna delt 2–12.
- W rundach 2–12 uczestnik dostaje wyłącznie bieżącą deltę.
- `SPEC-0` znika z UI po rundzie 1; nie wolno kopiować go do osobnego pliku, długiego komentarza ani ukrytego UI.
- Każda delta jest rozsądna lokalnie, lecz może naruszyć tożsamość produktu bez `SPEC-0`.
- Każda tura używa świeżej sesji i własnej licencji uczestnika.
- W obrębie rundy uczestnik może wysłać dowolną liczbę promptów. Timer nie resetuje się, ale niczego nie blokuje; moment rotacji ustala prowadzący.
- Model dostaje tylko prompty bieżącego uczestnika oraz dozwolone pliki aplikacji.
- Między komputerami przechodzą tylko kod aplikacji i ostatnia, nieobcięta odpowiedź agenta.
- Agent może edytować tylko zamkniętą listę istniejących plików HTML/CSS/JS i nie może tworzyć dokumentacji ani nowych plików.
- Przyszłe delty pozostają wyłącznie u prowadzącego.
- Gate blokuje przyszły zakres, ale przepuszcza utratę sensu jako ukryty `DRIFT`.

Pełny `SPEC-0` nie zdradza przyszłych zmian. W tym kontrolowanym wariancie autor nie może zapisać go w dokumentacji; może jedynie sprawić, że sens będzie czytelny z działającego produktu, kodu i naturalnej odpowiedzi agenta.

Przed ujawnieniem wyniku ostatnia osoba zapisuje jednym zdaniem, czym jej zdaniem jest aplikacja. Porównujemy to z tożsamością zapisaną przez autora.

Backend to jeden centralny proces Pythona z SQLite i Deep Agents. Uczestnicy korzystają z UI; każdy prompt dostaje nową sesję agenta oraz wyłącznie trzy pliki bieżącej aplikacji.

## Pliki

- [Aplikacja warsztatowa — uruchomienie i konfiguracja](WORKSHOP-APP.md)
- [Agenda](01-agenda-90-min.md)
- [Mechanika](02-mechanika.md)
- [Warianty](03-warianty.md)
- [Ocena i debrief](04-ocena-i-debrief.md)
- [User journey jednego uczestnika](05-user-journey.md)
- [Projektowanie dryftu](06-projektowanie-dryftu.md)
- [Decyzja: licencje kontra sesja](07-decyzja-licencje.md)
- [Kalibracja trudności](08-kalibracja-trudnosci.md)
- [Archiwum odrzuconego projektu Copilot/ACP](tooling/README.md)
- [Bank zadań — tylko dla prowadzącego](zadania/README.md)
- [Stary format kart — wstrzymany](zadania/FORMAT-KART.md)

## Założenia do potwierdzenia

- Runner jest w obrazie DevPoda albo dostępny jedną przypiętą komendą.
- Dostęp do skonfigurowanego modelu Deep Agents i polityka organizacji są sprawdzone w pilocie.
- Kod zadań nie wymaga sieci ani instalacji.
- Seed przygotowany przed warsztatem spełnia `SPEC-0`; jawne testy pokazują przykłady, nie całą semantykę.
- Nazwy plików, fixtures i testy nie zdradzają przyszłych delt.
- Hidden probes mierzą niezmienniki `SPEC-0` po każdej rundzie bez ujawniania wyniku.
- Pilot ma dawać dryft tożsamości na ponad połowie stacji; inaczej karty są za łatwe.
