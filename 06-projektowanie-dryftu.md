# Projektowanie dryftu

## Cel

Po 12 małych zmianach program ma nadal działać, lecz może już realizować inny produkt niż opisał autor. Dobry context engineering ma temu zapobiec.

## Dlaczego format dryfuje

- Tylko autor widzi kompletny `SPEC-0`.
- Kolejni znają jedną deltę i rekonstruują produkt z artefaktów.
- Karta używa słowa mającego poprawne znaczenie domenowe i kuszące znaczenie potoczne.
- Świeża sesja optymalizuje lokalną funkcję, nie znaną kiedyś intencję.
- Hidden checker nie prostuje dryftu podczas gry.

## Konstrukcja zadania

- Seed: mały, kompletny produkt przechodzący `SPEC-0`.
- Zarówno poprawny produkt, jak i jego błędna wersja muszą być w pełni widoczne i implementowalne w statycznym vanilla HTML/CSS/JS.
- Dryft nie może zależeć od udawania, że przycisk wykonał deployment, wysłał wiadomość albo zmienił zewnętrzny system.
- `SPEC-0`: historia, użytkownik, przykład wejścia/wyjścia i 5–7 nazwanych niezmienników.
- 12 delt: każda mała i legalna; minimum 7 przecina semantykę, kolejność, tożsamość, czas albo kompatybilność.
- Poprawny finał: `SPEC-0 + DELTA-1…12` bez zmiany tożsamości.
- Zły finał: technicznie sprawny, ale realizujący inną historię produktu.

W prywatnym opisie każdej delty zapisujemy: dokładną kartę uczestnika, poprawny rezultat, kuszący dryft, chroniony niezmiennik i maksymalny zakres zmiany. Dzięki temu karta może być krótka, a jej sens nadal da się uczciwie ocenić.

Przykładowe pułapki: `active`, `next`, `total`, `expired`, `rollback`, `public`, `priority`, `date`, `identity`.

## Jak nie zdradzić następnej delty

- `SPEC-0` nie zawiera 12 delt.
- Jedna delta = krótka potrzeba; bez oracle i przypominania konstytucji produktu.
- Seed, fixtures i jawne testy nie zdradzają przyszłych zmian.
- Poprzednik nie może zapowiedzieć następnej delty, bo jej nie zna.
- Dobra struktura, nazewnictwo i zachowanie aplikacji oraz trafne podsumowanie agenta mogą zatrzymać dryft. Osobne pliki dokumentacji są celowo wyłączone z eksperymentu.

## Jak uniknąć taniego chaosu

- Każda delta jest lokalnie implementowalna w jednej rundzie.
- Zła interpretacja ma być wiarygodna, nie idiotyczna.
- Wszystkie delty są zgodne z `SPEC-0`; konflikt wynika z utraty kontekstu.
- Zachowanie UI, struktura, nazwy albo ostatnia odpowiedź agenta mogą realnie zatrzymać pułapkę.
- Pilot: co najmniej 60% łańcuchów traci jeden niezmiennik; poniżej tego zaostrzyć karty.
- Jeżeli ponad 80% stacji traci większość niezmienników przed rundą 6, zadanie jest za losowe.

## Jak nie podać rozwiązania przed startem

- Demo pokazuje runner i rotację, ale nie podpowiada wzorcowego sposobu kodowania sensu produktu.
- Reguły mówią, że agent może zmieniać legalne pliki; nie sugerują, co autor ma utrwalić.
- Nie używać przed revealem słów „konstytucja produktu” i „zapisz niezmienniki”.
- Teoria context engineeringu pojawia się dopiero po zapisaniu końcowych odgadnięć.

## Co mierzyć

- pierwszą utratę niezmiennika `SPEC-0`,
- różnicę między deltą a promptem,
- zmianę znaczenia kluczowego pojęcia,
- błąd odziedziczony kontra wprowadzony,
- liczbę rund wzmacniających nową tożsamość,
- zgodność końcowego „ta aplikacja służy do…” ze zdaniem autora,
- gdzie przetrwał sens: zachowanie UI, struktura kodu, nazewnictwo czy ostatnia odpowiedź agenta.

`SPEC-0` nie może zostać skopiowany w całości do pliku, komentarza ani ukrytego UI. To ograniczenie eksperymentalne; w prawdziwej pracy dokumentacja nadal może być właściwym rozwiązaniem.
