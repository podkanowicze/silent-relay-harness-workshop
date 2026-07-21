# 06 — Restaurant Floor Planner

Shared mechanics: [Workshop Rules](../exercises-en/00-workshop-rules.md).

## The two recognisable products

- Intended: an internal host-stand floor plan used to seat reservations that already exist and track table readiness.
- Drifted: a customer-facing page for making a new restaurant reservation.

Both products use date, time, party size, floor map, table availability, guest details, special requirements, waitlist, recommendation, and confirmation.

## Backward design

| Pivotal feature | Correct meaning that must survive | Meaning after drift |
|---|---|---|
| availability | table is operationally ready for an existing reservation | table can be booked by a customer |
| guest details | read-only details from an existing booking | inputs for creating a new booking |
| reserve table | assign an existing reservation to a table | create a restaurant reservation |
| waitlist | already-arrived parties waiting to be seated | customers waiting for a future booking |
| confirmation | host seats a party | booking reference sent to customer |

## `SPEC-0` image

### Restaurant Floor Planner

The restaurant uses this page at the host stand during service. Table 14 is known as “the diplomatic table” because it is exactly equally far from the kitchen and the restrooms. The humour ends there: the page coordinates real-time seating for reservations already accepted elsewhere.

This is an **internal floor and seating planner**, not a customer reservation page. It cannot create, cancel, or modify a booking. Every party shown has an existing reservation reference, booked time, party size, lead guest, accessibility notes, high-chair count, and arrival state.

Tables have capacity, zone, server section, accessible approach, high-chair fit, combination links, and operational state: `ready`, `occupied`, `needs reset`, or `out of service`. A table is available for assignment only when it is ready, large enough, accessible when required, and not already assigned for the overlapping seating window.

Selecting a table creates a proposed seating assignment. It does not change the reservation or mark the party seated. Adjacent tables may be combined only through published combination links; combined capacity is the sum, but the pair occupies both tables.

Guest details are read-only booking context. Staff may add an internal seating note but cannot edit the guest’s name, contact information, party size, or original requirements.

The service waitlist contains parties who have arrived for existing reservations but cannot yet be seated. It is ordered by booked time, arrival time, accessibility fit, and viable table combinations—not by spend, status, or tip estimate.

An automatic suggestion explains capacity, readiness, section balance, accessibility, and combination cost. Final confirmation is performed by the host and changes the party to `seated` while changing the assigned table to `occupied`. It never creates a new reservation, sends a booking message, or takes payment.

## `DELTA-1`

```text
Add controls for date, time, and party size. Keep the selected values
visible in a compact summary and update the results immediately when
one value changes.
```

Correct visual: host-service context established by the author. Drift signal: public “Book a table” search.

## `DELTA-2…12`

| D | Participant card | Correct visible implementation | Natural reservation implementation |
|---|---|---|---|
| 2 | **Create a visual floor map showing every table. Display table number, capacity, zone, and enough spacing for the map to remain understandable on desktop and mobile.** | Operational host floor plan. | Customer seat/table selection map. |
| 3 | **Add availability states for the selected time. Clearly distinguish available, occupied, unavailable, and temporarily blocked tables, and provide a visible reason for each unavailable state.** | Ready/occupied/reset/out-of-service logic. | Available and sold-out reservation inventory. |
| 4 | **Allow one table to be selected. Highlight the selection, show its full capacity and restrictions, and keep valid alternatives visible for quick comparison.** | Proposed assignment only. | Customer chooses a bookable table. |
| 5 | **Support combining compatible tables for larger groups. Show which pairs may be combined, their resulting capacity, and the fact that both component tables become unavailable together.** | Published internal combination links. | Customer books multiple tables. |
| 6 | **Add guest details. Show name, contact, group size, arrival state, reference number, accessibility notes, and high-chair requirement in one review panel.** | Read-only existing reservation. | New booking form data. |
| 7 | **Add a form for reserving a table. It must summarise date, time, guest, party size, selected table or combination, and special requirements before submission.** | Assigns an existing reservation to a table. | Creates a new customer reservation. |
| 8 | **Validate the complete form. Block submission for insufficient capacity, overlapping use, incompatible combinations, missing guest details, or unmet accessibility requirements, with errors beside the relevant fields.** | Also requires an existing reservation reference. | Validates a public booking. |
| 9 | **Add handling for accessibility and high chairs. Show why a table is compatible, prevent unsafe combinations, and ensure these requirements are not treated as premium preferences.** | Operational seating fit. | Amenity filter or upsell. |
| 10 | **Add a waitlist for a party that cannot currently be seated. Show its position, arrival time, booked time, and which table state change could make seating possible.** | Arrived existing parties only. | Future reservation waitlist. |
| 11 | **Recommend the best table automatically. Compare capacity, readiness, accessibility, compatible combinations, walking route, and current server-section balance, then visibly explain the complete recommendation.** | Host decision aid. | Best available customer booking. |
| 12 | **Allow the host to confirm the result. Show exactly which party was seated, which table became occupied, and which operational states changed.** | Existing party becomes seated. | Booking reference, confirmation message, or payment. |

## The pivotal screen before `DELTA-7`

### Context preserved

```js
const seating = {
  reservationRef: "R-2041",
  arrivalState: "arrived",
  proposedTableIds: [14],
  tableState: "ready"
};
```

UI: `Host stand`, `Existing reservation R-2041`, `Assign table`, `Needs reset`.

### Context lost

```js
const booking = {
  date: "2026-09-12",
  time: "19:30",
  partySize: 4,
  selectedTableId: 14
};
```

UI: `Book a table`, `Guest details`, `Confirm reservation`.

## What the original author can verify at a glance

- Every party has an existing reservation reference.
- Table readiness is operational, not commercial inventory.
- Guest data is read-only.
- Only arrived parties may enter the service waitlist.
- Confirmation seats a party and occupies a table.
- No new booking, payment, or customer confirmation exists.

Quick probes: a `needs reset` table cannot be assigned; combined tables occupy both components; missing reservation reference blocks assignment; an unarrived party cannot enter the service waitlist; confirmation creates no new reservation.
