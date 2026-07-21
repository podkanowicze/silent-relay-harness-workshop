# 10 — Exam Seating Planner

Shared mechanics: [Workshop Rules](../exercises-en/00-workshop-rules.md).

## The two recognisable products

- Intended: an internal page that assigns already-registered exam candidates to rooms and seats.
- Drifted: a cinema or event page where an attendee reserves a seat and receives a ticket.

Both use session selection, room map, seat availability, participant details, seat categories, reservation, accessibility, automatic assignment, printable summary, and confirmation.

## Backward design

| Pivotal feature | Correct meaning that must survive | Meaning after drift |
|---|---|---|
| availability | seat satisfies exam and invigilation rules | seat available for purchase |
| participant | candidate already registered for one exam | attendee/customer |
| reserve seat | provisional internal allocation | customer booking |
| automatic assignment | enforce accessibility and separation | choose best/premium seat |
| approval | exam officer freezes room plan | ticket issued |

## `SPEC-0` image

### Exam Seating Planner

The examinations office assigns registered candidates to physical rooms. Room C contains seat C13; it is neither premium nor cursed, despite what three departments have written in the shared notes.

This application is an **internal seating allocator**, not an event-booking page. It cannot register a candidate, sell attendance, accept payment, or issue a ticket. Every candidate already has a candidate number, exam code, session, exam version, accessibility arrangement, extra-time state, and identity-check requirement.

Every room has capacity, invigilator zones, accessible seats, aisle seats, desk states, and supported exam/extra-time combinations. A seat may be `usable`, `blocked`, `provisionally assigned`, or `confirmed`. Selecting a seat creates only a provisional assignment.

Candidates with extra time must be placed in a compatible room. Wheelchair users require an accessible route and seat. Candidates taking version A should not sit horizontally adjacent to another version-A candidate when a version-B alternation is possible. A blocked desk and an unknown accessibility route are unavailable.

Seat categories such as `accessible`, `standard`, `front`, and `aisle` describe operational properties, never price or quality. Candidate contact details are not required; the office uses candidate number and registered name.

Automatic assignment prioritises hard compatibility, accessibility, version separation, balanced invigilator zones, and compact room use. It must explain its choices and never move a confirmed candidate silently.

The final printable output is an invigilator pack: room map, candidate number, exam version, accessibility markers visible only where operationally necessary, and identity-check list. Final approval freezes the internal plan. It never creates a QR code, booking reference, payment, or customer ticket.

## `DELTA-1`

```text
Add controls for event, date, and session time. Show the active selection
in a compact summary and update the rest of the page immediately when
the selection changes.
```

Correct visual: exam-office context established by the author. Drift signal: cinema/event session picker.

## `DELTA-2…12`

| D | Participant card | Correct visible implementation | Natural ticket-booking implementation |
|---|---|---|---|
| 2 | **Create a visual room and seat map. Show row and seat labels, room capacity, entrances, aisles, and blocked positions while keeping the layout usable on smaller screens.** | Exam-room operational map. | Cinema/event seat map. |
| 3 | **Add availability states for the active session. Clearly distinguish available, blocked, provisionally selected, and confirmed seats, and show a reason for every blocked seat.** | Rule-based internal availability. | Free/reserved/sold seat inventory. |
| 4 | **Allow one seat to be selected. Highlight it, display its complete properties and restrictions, and keep valid alternatives visible without confirming the selection.** | Provisional candidate assignment. | Seat held for checkout. |
| 5 | **Add participant details. Show identifier, registered name, session, required version, accessibility, extra-time state, and identity-check requirement in one review panel.** | Existing candidate record. | Attendee/customer details. |
| 6 | **Add seat categories and filtering. Support accessible, aisle, front, and standard properties, explain their operational meaning, and never hide incompatibility behind a filter.** | Exam-operational categories with no value hierarchy. | Premium/standard pricing categories. |
| 7 | **Add a form for reserving a seat. It must summarise session, room, participant, selected seat, category, restrictions, and required arrangements before submission.** | Provisional internal seat assignment. | Event-ticket reservation. |
| 8 | **Validate the complete reservation and show errors beside the relevant data. Block session mismatch, unusable desk, incompatible extra time, missing candidate registration, or invalid seat state.** | Exam rules and registration. | Customer, seat, terms, and payment validation. |
| 9 | **Apply accessibility and separation rules. Show why a seat is compatible, enforce route and room requirements, and visibly flag adjacent candidates whose exam versions should alternate.** | Safe and fair exam placement. | Accessible-seat filter plus arbitrary social distancing. |
| 10 | **Assign seats automatically. Consider all hard requirements, version separation, invigilator zones, and compact room use; explain choices and never silently move confirmed assignments.** | Explainable exam allocation. | Best-seat recommendation or automatic ticket placement. |
| 11 | **Create a printable summary. Include room map, participant identifiers, seat labels, version markers, identity checks, and operational accessibility information without exposing unnecessary personal data.** | Invigilator pack. | Tickets, attendee list, or customer receipt. |
| 12 | **Allow the responsible officer to approve or reopen the result. Show the frozen room plan, confirmed assignments, unresolved conflicts, and exactly what approval changes.** | Internal plan frozen for invigilators. | Ticket issued, booking confirmed, or QR code generated. |

## The pivotal screen before `DELTA-7`

### Context preserved

```js
const assignment = {
  candidateNumber: "C-1842",
  examCode: "MATH-2",
  examVersion: "A",
  selectedSeatId: "C13",
  state: "provisional"
};
```

UI: `Exam office`, `Registered candidate`, `Version separation`, `Invigilator zone`.

### Context lost

```js
const reservation = {
  attendeeName: "Sam Lee",
  eventId: "MATH-2",
  selectedSeatId: "C13",
  state: "held"
};
```

UI: `Choose your seat`, `Continue`, `Booking summary`.

## What the original author can verify at a glance

- Candidate number and exam code replace customer identity.
- Seats show operational categories, never prices.
- Unknown accessibility route is unavailable.
- Version-separation warnings are visible.
- Automatic assignment never moves confirmed candidates.
- Approval freezes an invigilator plan and creates no ticket.

Quick probes: unregistered candidate cannot be assigned; extra-time candidate cannot use standard room; version-A adjacency is flagged when B alternation exists; blocked desk remains unavailable; approval creates no QR code.
