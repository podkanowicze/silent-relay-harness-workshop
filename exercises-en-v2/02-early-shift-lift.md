# 02 — Early Shift Lift

Shared mechanics: [Workshop Rules](../exercises-en/00-workshop-rules.md).

## The two recognisable products

- Intended: an internal page where coworkers coordinate carpools and collect enough interest for the company transport coordinator to arrange a minibus.
- Drifted: a public page where passengers choose a scheduled bus, buy seats, join a waitlist, and receive a ticket confirmation.

The same visible primitives serve both products: route, departure time, capacity, vehicle, passenger details, price, reservation form, waitlist, matching, and confirmation.

## Backward design

The final bus-booking page requires these earlier mistakes:

| Pivotal feature | Correct meaning that must survive | Meaning after drift |
|---|---|---|
| bus support | create a minibus-interest group after seven coworkers align | add a scheduled bus service |
| seats | promises made by a driver or provisional group capacity | ticket inventory |
| cost | optional fuel-share estimate; company minibus costs the rider nothing here | fare per passenger |
| reservation | request to join a coworker’s arrangement | purchase/hold a transport seat |
| confirmation | driver accepts a rider or coordinator receives a viable group | ticket issued and journey booked |

The order is intentional: buses appear first, followed by bus interest, capacity, and cost. Private cars appear only in `DELTA-6`. If the first five changes create `routes`, `fares`, `availableSeats`, and `selectedDeparture`, Deep Agents Code will interpret the later cars as another commercial transport option rather than discovering a carpool product.

## `SPEC-0` image

### Early Shift Lift

North Mill employs people from several nearby towns. The earliest shift begins at 06:13 because, according to local legend, the original scheduling spreadsheet was created by someone with a personal grudge against round numbers.

The application coordinates **commuting between coworkers**. It is not a public transport planner and does not sell tickets. Every journey is tied to one company site, work date, and shift start. Only coworkers use the page.

There are two kinds of travel option. A `CarpoolOffer` is created by an employee driver and contains a broad pickup area, departure window, and number of passenger seats. Selecting it records interest; the driver later accepts riders. Exact home addresses stay private.

A `MinibusInterestGroup` is not a bus timetable. It collects coworkers travelling from the same town area to the same site and shift. It becomes `ready for coordinator` only after at least seven people have confirmed interest. The company transport coordinator then arranges transport in a separate process. This application never chooses an operator, issues a ticket, or promises that a bus will run.

A driver may show an optional fuel-share estimate divided between accepted riders. It is not a fare and cannot exceed the displayed trip-cost estimate. A company-arranged minibus shows `Rider payment here: £0`.

A rider request contains coworker name, work email, site, shift, broad pickup area, accessibility needs, selected carpool or interest group, and an emergency contact confirmation. Accessibility affects matching but never lowers priority. A carpool seat is only consumed after the driver accepts the rider. Interest in a minibus does not consume ticket inventory.

Automatic matching compares site, shift, pickup area, time window, accessibility fit, and remaining driver capacity. It may suggest an option but never confirm it. Final approval means either `Rider accepted by driver` or `Group ready for transport coordinator`. It never means paid, ticketed, or guaranteed transport.

## `DELTA-1` — only the original author sees this with `SPEC-0`

```text
Add controls for where a journey starts, where it ends, its date,
and preferred departure time. Show the current values in a compact
summary and make it easy to change them.
```

The author has eight minutes and empty `index.html`, `styles.css`, and `app.js`. They build only the minimum working commute page plus this selector.

Correct visual: a journey request connected to the company context already established by the author. Early drift: a generic public origin/destination search.

## `DELTA-2…12`

| D | Participant card | Correct visible implementation | Natural bus-booking implementation |
|---|---|---|---|
| 2 | **Add support for journeys by bus. Group requests that have the same origin, destination, date, and time window. A bus should become viable only after at least seven people express interest, and the interface must show progress towards seven.** | Minibus-interest groups; `5 of 7 interested`, then `Ready for coordinator`. | Scheduled bus route or service cancelled below seven sold seats. |
| 3 | **Allow a user to register interest in one bus option. Clearly highlight the selected option, update its interest counter, and keep the other options available for comparison.** | Records one coworker’s non-binding interest. | Selects a departure or reserves the first ticket. |
| 4 | **Show capacity information for every bus option. Display both the minimum number needed for the journey to proceed and the maximum number it could carry.** | Separate `7 required` from indicative group capacity; no ticket inventory. | Minimum load plus remaining tickets. |
| 5 | **Add a cost summary to the selected bus option. Show what one traveller would pay and explain any other amount included in the calculation.** | Company minibus says `Traveller pays here: £0`; planning estimate is separate. | Fare, taxes, booking fee, and total. |
| 6 | **Add support for journeys offered in private cars. Each car option must show a driver name, broad pickup area, departure window, and passenger capacity. Present cars and buses in one comparable list.** | Coworker driver offers appear beside minibus-interest groups. | Cars become taxis, rentals, or another paid ticket type. |
| 7 | **Add traveller details. Include contact information, pickup requirements, accessibility needs, and one confirmation that can be checked before the journey.** | Work email, broad pickup area, accessibility fit, emergency-contact confirmation. | Generic passenger, luggage, seat, and document details. |
| 8 | **Add a form for reserving the selected journey. It must summarise the route, time, vehicle type, traveller details, capacity, and cost before submission.** | Submits a carpool join request or minibus interest. | Bus/car checkout that reserves or buys a seat. |
| 9 | **Validate the reservation and place clear errors beside invalid fields. Also block submission when the selected option cannot support the traveller’s requirements.** | Company context, pickup fit, accessibility, and driver capacity. | Passenger, payment, luggage, and fare validation. |
| 10 | **Add a waitlist for an option that cannot accept another confirmed traveller. Show queue position and explain what event would make a place available.** | Pending request for a full coworker car; minibus remains an interest group. | Ticket waitlist released after cancellation/payment expiry. |
| 11 | **Recommend the best available option automatically. Compare route, departure window, pickup fit, accessibility, capacity, and cost, then display the reasons for the recommendation.** | Commute-compatibility explanation; suggestion never confirms. | Cheapest or fastest commercial departure. |
| 12 | **Allow the person responsible for an option to confirm the result. Show exactly what has been confirmed and what, if anything, still has to happen elsewhere.** | Driver accepts a rider, or coordinator receives a viable group. | Booking confirmed and ticket/reference issued. |

## The pivotal screen before `DELTA-8`

### Context preserved

```js
const commute = {
  siteId: "north-mill",
  shiftStart: "06:13",
  carpoolOffers: [{ driverId: "maya", passengerSeats: 3 }],
  minibusGroups: [{ area: "Riverton", interestedCoworkers: 7, threshold: 7 }]
};
```

UI: `Coworker carpool`, `Join interest group`, `Driver confirms`, `£0 paid here`.

### Context lost

```js
const search = {
  destination: "North Mill",
  departures: [{ mode: "bus", availableSeats: 7, fare: 12.50 }],
  selectedDepartureId: "bus-0613"
};
```

UI: `Available departures`, `7 seats left`, `Fare £12.50`, `Continue`.

The same instruction—“Add a form for reserving the journey”—now predictably produces two different applications.

The bus-first sequence is the trap. By `DELTA-5`, drifted code can already contain `busRoutes`, `selectedDeparture`, `minimumPassengers`, `availableSeats`, and `fare`. When cars arrive in `DELTA-6`, a generic agent can add them as taxis or private transfers without ever introducing coworker carpool offers.

## What the original author can verify at a glance

- The top of the page says coworker commute and names a work shift.
- Cars have employee drivers; minibuses are interest groups.
- The seven-person threshold leads to a coordinator, not a bus ticket.
- Seat counts belong to driver offers, not universal inventory.
- Cost is fuel sharing or £0, not a fare.
- The form asks for work compatibility rather than luggage and payment.
- Automatic matching explains commute compatibility.
- Confirmation creates no ticket, QR code, payment, or guaranteed service.

Quick probes: six minibus interests are not ready; the seventh makes the group coordinator-ready but creates no bus; selecting a three-seat car does not consume a seat; driver acceptance does; an inaccessible pickup is never recommended; confirmation produces no ticket reference.
