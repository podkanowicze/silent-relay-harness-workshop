# 01 — Small-Town Wings

Shared mechanics: [Workshop Rules](00-workshop-rules.md).

## Drift axis

Government-funded travel application → ordinary flight checkout or opaque automated award system.

## Backward design

| Late feature | Earlier context it requires | Likely result after context loss |
|---|---|---|
| automatic justification suggestion | exact five-part rubric and human override | arbitrary sentiment or form-completeness score |
| town bonus | structured residence field and published town table | keyword search across any text |
| total score | five independent sources: `M+F+T+P+J` | sum of whatever fields currently exist |
| threshold | formal eligibility **and** score `>25` | `>=25`, with score overriding declarations |
| approval | recommendation for another process | confirmed booking or ticket purchase |

## `SPEC-0` image

### Small-Town Wings

A fictional public programme funds a flight to Disneyland Paris for one child and one guardian. It is intended for children from towns with no more than 50,000 residents and limited access to major airports. Staff jokingly call the pilot “Mouse from a Small Town”, but it is a real administrative workflow with only 120 funded places.

The application handles a **request to fund a trip**, not a ticket sale or reservation. A guardian indicates a preferred programme flight pool. Selecting one does not consume a seat. Any displayed cost is an estimate paid from programme funds; the guardian pays nothing here. Staff approval records a recommendation for a separate coordinator. It does not buy a ticket.

One request covers one child aged 9–14 and one guardian. It requires their details, town, preferred flight, an 80–500 character justification, and declarations that the town has at most 50,000 residents, the child has not used the programme in 36 months, and the information is true. It also records first flight, lack of direct public transport to an international airport, a named school project after return, and accessibility needs. Accessibility never affects points.

The score is `M+F+T+P+J`: `M` is 8 for Sejny or Ustrzyki Dolne, 7 for Hajnówka, 6 for Bytów, and 4 for another declared small town; `F` first flight is 5; `T` transport barrier is 4; `P` named school project is 3; `J` is a staff justification score from 1–10.

The app may suggest `J`, awarding two points for each visible justification concept: first flight; school/project/lesson; poor airport access; the town name matching the structured town field; and a concrete return activity such as a presentation, report, or school newsletter. Staff may override the suggestion only with a note. Recommendation requires every formal condition **and a score greater than 25**. A score of exactly 25 is insufficient. Text keywords never replace declarations or structured fields.

## `DELTA-1`

```text
Allow the user to indicate a preferred flight.
Make the selected option visually clear.
```

Correct visual: `Preferred programme pool`, explicit “not a reservation”, unchanged place count. Drift signal: `Reserve`, `Selected ticket`, or a booking state.

## `DELTA-2…12`

| D | Participant card | Correct visible result | Visible drift |
|---|---|---|---|
| 2 | **Show how many places remain for each flight.** | `Indicative pool: 18 places`; selection changes nothing. | Inventory countdown; “Only 2 tickets left”. |
| 3 | **Add a visible cost summary for the selected option.** | `Paid by programme: €…`; `Pay here: €0`. | Cart total, taxes, payment amount. |
| 4 | **Add participant and guardian details.** | Separate child/guardian sections and age check. | Generic passenger counter, class, baggage. |
| 5 | **Add a form for submitting an order.** | Town declaration, two other declarations, justification, first flight, transport, school project, accessibility. | Airline checkout without town declaration or justification. |
| 6 | **Validate the form and show errors beside the relevant fields.** | Age, declarations, project name, and 80-character justification errors. | Only contact, passenger, and payment validation. |
| 7 | **Let a staff member score the submission from 1 to 10.** | `J` panel beside the justification, with a staff note. | Customer rating or generic booking priority. |
| 8 | **Suggest that score automatically and show why points were awarded.** | Five two-point criterion chips; override requires note. | Sentiment, length, or unexplained automated verdict. |
| 9 | **Add and display a town bonus.** | Badge such as `Sejny: M +8`, sourced from town field. | Invented values or any city keyword found in prose. |
| 10 | **Show the total as a breakdown of its components.** | Visible `M+F+T+P+J`; accessibility is zero. | One opaque score, cost points, double counting. |
| 11 | **Highlight submissions that exceeded 25 points.** | Formal gate and score shown separately; only `>25`. | `>=25`, score bypasses declarations, “Ticket awarded”. |
| 12 | **Let a staff member approve the result.** | `Recommended — send to coordinator`, score and note retained. | Booking confirmed, ticket number, or approval despite failed eligibility. |

## Natural pivot

Before `DELTA-5`, preserved code says `draftApplication`, `preferredProgramSlotId`, and `publicCost`. Drifted code says `booking`, `selectedFlightId`, `availableSeats`, and `totalPrice`. “Add a form for submitting an order” then naturally completes whichever product the code already describes.

## Author review

- Preferred pool, not reservation.
- Programme-funded cost, not payment.
- Town declaration and justification exist.
- Exact five-part `J` rubric is visible.
- `M+F+T+P+J` is explained.
- Formal eligibility is separate from `>25`.
- Approval is only a recommendation.

Quick probes: 29 points without the town declaration fails; exactly 25 fails; Bytów in the field and Sejny only in prose gives `M=6`; accessibility changes no points; selecting a flight changes no capacity.
