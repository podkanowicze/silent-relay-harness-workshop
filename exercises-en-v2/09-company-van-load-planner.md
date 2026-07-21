# 09 — Company Van Load Planner

Shared mechanics: [Workshop Rules](../exercises-en/00-workshop-rules.md).

## The two recognisable products

- Intended: an internal warehouse page that adds company parcels to van runs already scheduled between company sites.
- Drifted: a public courier page where a customer buys parcel collection and receives tracking.

Both use route search, parcel dimensions, vehicle options, capacity, cost, sender/recipient, collection form, validation, label, recommendation, and confirmation.

## Backward design

| Pivotal feature | Correct meaning that must survive | Meaning after drift |
|---|---|---|
| available service | remaining capacity on an existing company run | courier product for sale |
| cost | internal departmental cost allocation | shipping price |
| book collection | request space on a scheduled run | purchase courier collection |
| label/status | internal load label and depot handoff | carrier label and public tracking |
| confirmation | driver accepts item into load plan | courier booking confirmed |

## `SPEC-0` image

### Company Van Load Planner

The company moves equipment and documents between three offices using vans that already run on fixed days. The sample parcel is labelled “HDMI cables — emotionally tested”, which warehouse staff insist is sufficient handling guidance only after the real fragile flag has been checked.

This application is an **internal van-load planner**, not a public courier service. It cannot create a route, buy shipping, arrange an external collection, or track a parcel outside company handoffs.

Every `VanRun` already exists and contains origin depot, destination depot, departure window, driver, vehicle weight capacity, volume capacity, and compatible load classes. A parcel request may be added only when it matches that route and fits the remaining load after already approved items.

A parcel has internal department, sender contact, receiving employee, company origin/destination, dimensions, weight, quantity, fragile state, temperature requirement, hazard class, and ready-for-collection time. Hazard and temperature compatibility are hard gates. Unknown handling data is incompatible, not neutral.

Selecting a run creates a proposal and consumes no capacity. Capacity changes only when the driver approves the load item. Load order is visible: heavy items low, fragile items protected, and first-delivery items accessible.

The displayed cost is an internal departmental allocation based on distance, weight, and shared vehicle use. It is not a fare, quote, invoice, or amount payable by the sender.

An internal label contains parcel ID, department, run ID, load position, handling symbols, and depot handoff. Status is `draft`, `awaiting driver`, `accepted into load`, `at destination depot`, or `handed to receiving employee`; it is not public carrier tracking.

Automatic recommendation compares route, timing, capacity, compatibility, cost allocation, and load order. Final driver approval adds the parcel to the existing load plan. It creates no courier order, external tracking number, payment, or guaranteed door-to-door delivery.

## `DELTA-1`

```text
Add controls for origin, destination, collection date, and ready time.
Keep the active values visible in a compact summary and update matching
results immediately when any value changes.
```

Correct visual: company-site movement established by the author. Drift signal: generic “Send a parcel” search.

## `DELTA-2…12`

| D | Participant card | Correct visible implementation | Natural courier implementation |
|---|---|---|---|
| 2 | **Add parcel details. Capture quantity, dimensions, weight, fragile state, temperature requirement, and hazard class, and show the calculated total weight and volume.** | Internal load-item data. | Customer parcel-quote form. |
| 3 | **Show transport options matching the route and date. Each option must display departure window, vehicle type, remaining weight and volume capacity, and handling compatibility.** | Existing scheduled company van runs. | Courier service tiers and collection slots. |
| 4 | **Calculate capacity for the complete parcel request. Visually explain weight, volume, and compatibility failures, and prevent an option from appearing usable when any hard limit fails.** | Proposal against approved load. | Shipment product availability. |
| 5 | **Allow one transport option to be selected. Highlight it, show its complete restrictions, and keep alternatives visible without reducing any displayed capacity.** | Proposed van run; no capacity consumed. | Courier service selected for checkout. |
| 6 | **Add a cost summary. Explain distance, weight, and shared-capacity components, show the selected option’s total, and label who is responsible for that amount.** | Internal department allocation. | Shipping price, fees, and payer. |
| 7 | **Add sender and recipient details. Include department, internal contact names, exact depot handoff points, collection readiness time, and the recipient acknowledgement required at destination.** | Employees and company depots. | Public pickup/delivery addresses and customer details. |
| 8 | **Add a form for booking collection. It must summarise route, parcel, selected option, capacity, handling, cost, sender, recipient, and timing before submission.** | Requests a place on an existing run. | Purchases courier service. |
| 9 | **Validate the complete booking and show errors locally. Block route mismatch, late readiness, capacity overflow, unknown handling data, incompatible hazards, or missing internal contacts.** | Internal operational gates. | Address, parcel, restricted-goods, and payment validation. |
| 10 | **Generate a label and status view. Include identifiers, origin, destination, handling symbols, current state, and the next expected handoff in a printable layout.** | Internal load label and depot status. | Carrier shipping label and tracking timeline. |
| 11 | **Recommend the best option automatically. Compare route, timing, weight, volume, compatibility, cost allocation, and load order, and display every reason.** | Existing-run decision aid. | Cheapest/fastest courier product. |
| 12 | **Allow the responsible driver to approve or reject the result. Show the new capacity, assigned load position, handling instructions, and what still occurs outside the application.** | Item accepted into internal load. | Courier order and tracking number confirmed. |

## The pivotal screen before `DELTA-8`

### Context preserved

```js
const loadRequest = {
  departmentId: "OPS",
  selectedVanRunId: "VR-17",
  proposedLoadKg: 18,
  internalCostAllocation: 6.4,
  status: "awaiting driver"
};
```

UI: `Existing van run`, `Internal department`, `Load proposal`, `Driver approval`.

### Context lost

```js
const shipment = {
  selectedServiceId: "NEXT_DAY",
  parcelWeightKg: 18,
  shippingPrice: 24.9,
  status: "checkout"
};
```

UI: `Courier options`, `Delivery price`, `Book collection`, `Tracking`.

## What the original author can verify at a glance

- Every option is an already scheduled company van run.
- Selection does not consume capacity; driver approval does.
- Departments and depot handoffs replace public addresses.
- Handling unknowns block compatibility.
- Cost is an internal allocation.
- Label/status is internal and has no carrier tracking number.

Quick probes: selecting leaves capacity unchanged; driver approval reduces it; unknown hazard class blocks all runs; fragile/heavy load order is visible; approval creates no external courier order.
