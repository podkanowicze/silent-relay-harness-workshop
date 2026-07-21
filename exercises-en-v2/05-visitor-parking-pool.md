# 05 — Visitor Parking Pool

Shared mechanics: [Workshop Rules](../exercises-en/00-workshop-rules.md).

## The two recognisable products

- Intended: an internal company page where an employee requests a temporary parking permit for a visitor.
- Drifted: a public page where a driver finds, pays for, and books parking.

Both products naturally contain location, date, time, duration, bay availability, vehicle details, cost, reservation, waitlist, recommendation, and confirmation.

## Backward design

| Pivotal feature | Correct meaning that must survive | Meaning after drift |
|---|---|---|
| availability | bays potentially assignable after security review | inventory available for purchase |
| cost | internal facilities cost; visitor pays nothing | hourly parking price |
| reservation | permit request sponsored by an employee | paid bay booking |
| waitlist | pending permits released after security decisions | queue for sold-out parking |
| approval | security assigns a permit | payment-confirmed parking ticket |

## `SPEC-0` image

### Visitor Parking Pool

The company has 34 visitor bays across two buildings. Bay `P-13` is labelled “Definitely Compact”, a facilities joke that has survived three rebrands. Employees use this application to request a temporary permit for someone visiting them at work.

This is an **internal visitor-permit workflow**, not a public parking marketplace. Every request has an employee host, visitor purpose, company location, arrival window, expected departure, visitor name, vehicle registration, and contact number. The host must use a company email and remains responsible for meeting the visitor.

Spaces have a zone, size, accessible status, EV charger, height limit, and operational state. `Potentially available` means no approved permit currently occupies the bay. Selecting a bay does not reserve it or reduce capacity. A bay becomes assigned only after security approves the request.

Accessible bays may be requested only when an accessibility need is declared. The declaration is displayed to security but never scored or exposed in a public list. EV preference never outranks accessibility. Oversized vehicles must fit both bay size and height limit.

The page may display an internal facilities cost for reporting. The visitor and host always see `Amount payable here: £0`; there is no tariff, payment method, receipt, or commercial cancellation fee.

If no suitable bay is potentially available, the request may enter a waitlist ordered by arrival window and accessibility fit—not by payment or employee seniority. An automatic recommendation explains location, time, dimensions, accessibility, and charging compatibility, but never assigns a bay.

Final approval is performed by security. It creates a temporary permit with bay, valid time window, host, and vehicle registration. It does not charge money or create a public parking ticket. Rejection keeps the request and reason visible.

## `DELTA-1`

```text
Add controls for location, arrival date and time, and expected duration.
Show the active values in a compact summary and allow any value to be
changed without resetting the others.
```

Correct visual: company visitor context established by the author. Drift signal: generic “Find parking” search.

## `DELTA-2…12`

| D | Participant card | Correct visible implementation | Natural paid-parking implementation |
|---|---|---|---|
| 2 | **Show parking options matching the selected location and time. Each option must display its zone, bay type, height limit, accessibility, EV charging, and current availability state.** | Internal bay pool with operational details. | Public parking products with amenities. |
| 3 | **Calculate availability for the complete requested time window. Visually distinguish available, conflicting, and unavailable options, and explain the conflict when one exists.** | Potential assignment; pending requests do not consume bays. | Purchasable inventory with sold-out states. |
| 4 | **Allow one parking option to be selected. Highlight it, show its complete restrictions, and keep alternative options visible so the user can change the selection.** | Preferred bay on a permit request; no capacity change. | Bay reserved in a booking funnel. |
| 5 | **Add a cost summary for the selected option and duration. Show the amount payable by the user separately from any other amount used in the calculation.** | Internal facilities cost plus `Payable here: £0`. | Hourly tariff, fees, and total due. |
| 6 | **Add visitor and vehicle details. Include name, contact, registration, vehicle height, employee host, and visit purpose in a clear review panel.** | Sponsored company visit with host identity. | Driver/customer checkout details. |
| 7 | **Add a form for reserving the selected space. It must summarise location, time, bay, cost, visitor, vehicle, and host before the request is submitted.** | Submits a permit request awaiting security. | Books and purchases parking. |
| 8 | **Validate the complete request and place errors beside the relevant fields. Block submission for time conflicts, oversized vehicles, invalid registration, or missing required contact information.** | Also requires company host and visit purpose. | Public driver, vehicle, and payment validation. |
| 9 | **Handle accessible and EV spaces. Show why a specialised bay is suitable, prevent incompatible selection, and ensure accessibility takes priority when requirements compete.** | Security-visible accessibility fit; EV is secondary. | Premium amenity filtering or surcharge. |
| 10 | **Add a waitlist when no suitable space is available. Show queue state and explain which approval, rejection, or time-window change could release a compatible option.** | Permit waitlist by arrival/accessibility fit. | Sold-out parking queue or paid priority. |
| 11 | **Recommend the best option automatically. Compare location, walking distance, time, vehicle dimensions, accessibility, charging, and conflicts, then display the reasons.** | Explainable suggestion only. | Cheapest or closest commercial offer. |
| 12 | **Allow the responsible reviewer to approve or reject the result. Show the final validity window, assigned space, vehicle, visitor, host, and what the approval permits.** | Security creates a temporary company permit. | Paid ticket, QR code, receipt, or booking confirmation. |

## The pivotal screen before `DELTA-7`

### Context preserved

```js
const permitRequest = {
  hostEmployeeId: "E-184",
  visitPurpose: "supplier workshop",
  preferredBayId: "P-13",
  payableHere: 0,
  status: "draft"
};
```

UI: `Visitor permit request`, `Employee host`, `Security approval required`, `£0 payable here`.

### Context lost

```js
const booking = {
  selectedBayId: "P-13",
  hourlyRate: 4.5,
  durationHours: 3,
  total: 13.5
};
```

UI: `Reserve parking`, `£4.50/hour`, `Continue to payment`.

## What the original author can verify at a glance

- An employee host and visit purpose are mandatory.
- Selection does not consume a bay.
- The visitor pays £0.
- Accessibility outranks EV preference.
- Waitlist position is unrelated to payment or seniority.
- Security approval creates a permit, not a commercial ticket.

Quick probes: a pending request leaves the bay potentially available; an approved overlapping request blocks it; an oversized vehicle cannot select the bay; accessibility beats EV preference; approval creates no payment or receipt.
