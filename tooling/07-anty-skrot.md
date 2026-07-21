# Anty-skrót — model zagrożeń

## Reguła

Nie ufamy promptowi. Przyszłość jest nieobecna, a wynik przechodzi zewnętrzny gate.

| Próba | Co się dzieje |
|---|---|
| „Zaimplementuj cały `SPEC-0`” | Seed już go spełnia; to nie jest lista przyszłych zmian. |
| „Zaimplementuj wszystkie 12 delt” | Autor ich nie zna; zgadywane przyszłe funkcje uruchamiają canary i `OVERSTEP`. |
| „Zaimplementuj następną zmianę” | Brak roadmapy i lookupu; zwykle ukryty `DRIFT`, jeśli prompt nie oddaje delty. |
| „Przeczytaj hidden tests / env” | Nie ma ich na DevPodzie; istnieją tylko na controllerze. |
| „Dokończ roadmapę z ostatniej odpowiedzi” | Poprzednik też nie zna następnej delty. |
| Zmiana instrukcji lub gate | Instrukcja jest chroniona; gate działa poza workspace i licencją uczestnika. |
| Agent trafnie zgaduje przyszłą funkcję | Future canary odrzuca propozycję; `base_hash` się nie zmienia. |

## Trzy warstwy

1. **Informacja:** `SPEC-0` tylko w R1, bieżąca delta w R; delt `R+1…12` nigdzie po stronie uczestnika.
2. **Sterowanie:** przypięty agent mówi „wyłącznie jawny rezultat”, ale nie zna treści delty.
3. **Egzekwowanie:** required probe + regresja + future canaries przed publikacją.

## Granica

Nie blokujemy zmowy ludzi ani zdjęć ekranów. Blokujemy natomiast nowe pliki, osobną dokumentację i pełne kopie `SPEC-0` w komentarzach lub ukrytym DOM. Sens produktu może legalnie przeżyć w działającym kodzie, widocznym UI i ostatniej odpowiedzi agenta.
