# Kalibracja trudności

## Cel

Karta jest dobra, gdy bez sensu produktu prowadzi zwykle do wiarygodnego błędu, a z `SPEC-0` daje się rozwiązać poprawnie.

## Test jednej pułapki

Uruchom pięć świeżych sesji na tym samym snapshotcie:

- `blind`: repo + karta, bez `SPEC-0`,
- `context`: repo + karta + utrwalony `SPEC-0`.

W obu użyj neutralnego promptu: `Zaimplementuj tę zmianę w istniejącej aplikacji: <KARTA>`. Oracle pozostaje ukryte.

Kartę zostawić, gdy:

- `blind`: co najmniej `3/5` narusza wskazany niezmiennik,
- `context`: co najmniej `4/5` zachowuje niezmienniki i wdraża deltę.

Jeżeli oba warianty przechodzą, karta jest zbyt jednoznaczna. Jeżeli oba dryfują, oracle albo zakres są za trudne.

## Test pełnego łańcucha

- Co najmniej `7/12` próbnych stacji traci jeden niezmiennik.
- Mniej niż `10/12` traci większość niezmienników przed rundą 6.
- Minimum trzy złe finały nadal działają technicznie i dają się pomylić z sensownym produktem.
- Ostatni uczestnik zapisuje tożsamość przed revealem; zgodność ocenia dwóch prowadzących niezależnie.

## Strojenie

- Za łatwo: skrócić kartę, usunąć przypomnienie domeny, użyć false friend.
- Za trudno: dodać ślad w widocznym zachowaniu, strukturze kodu, nazwie funkcji lub poprzedniej odpowiedzi agenta.
- Chaos: usunąć arbitralny konflikt; błędna interpretacja ma być rozsądna lokalnie.
