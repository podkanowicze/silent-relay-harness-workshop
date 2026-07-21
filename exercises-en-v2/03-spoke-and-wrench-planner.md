# 03 — Spoke & Wrench Planner

Shared mechanics: [Workshop Rules](../exercises-en/00-workshop-rules.md).

## The two recognisable products

- Intended: a shared internal to-do list and calendar for bicycle work already accepted by reception.
- Drifted: a customer-facing page for choosing a service, booking a time, seeing a price, and receiving appointment confirmation.

Both naturally contain a calendar, customer and bike details, service types, availability, price estimates, forms, validation, rescheduling, reminders, and confirmation.

## Backward design

| Pivotal feature | Correct meaning that must survive | Meaning after drift |
|---|---|---|
| availability | free space among existing tasks, required duration, and parts readiness | appointment slots offered to customers |
| service form | staff schedule tasks belonging to an accepted work order | customer orders a repair |
| price | internal estimate for reception to discuss separately | checkout price |
| confirmation | internal plan is added to the shared to-do calendar | customer appointment confirmed |
| reminder/finalise | internal parts, quality-check, and reception handoff | customer notification and completed booking |

The drift should be visible by the middle of the chain: navigation changes from `To-do / Calendar / Waiting for parts` to `Services / Pick a time / Your booking`.

## `SPEC-0` image

### Spoke & Wrench Workshop Planner

Spoke & Wrench repairs commuter bicycles. Reception accepts each bike, labels it, and creates a work order before it enters this application. The sample bike is a blue touring bicycle whose reported symptom is “the bell works perfectly, especially when braking”.

This application is a **shared internal to-do list and calendar**. It is not visible to customers and does not accept service orders or appointments. Every displayed bike is already physically at the shop and has an existing reception work-order number.

A `WorkOrder` contains read-only customer contact context, bike details, reported symptom, promised collection day, and reception notes. Staff do not edit the customer’s original report. They create ordinary to-do items such as diagnosis, parts check, repair, adjustment, road test, and quality check. Tasks may be open, completed, reopened, filtered, and placed on the calendar.

Calendar blocks reserve estimated time for internal tasks. “Available” means the required duration fits around existing work and all required parts are ready. It does not mean a time can be booked by a customer. The list is shared; this exercise does not assign tasks to individual mechanics. Reception remains responsible for customer communication.

Status is `awaiting diagnosis`, `planned`, `waiting for parts`, `in repair`, `quality check`, or `ready for reception`. `Ready for reception` does not mean collected, paid, or closed. Blocked parts remain visible and do not count as completed work.

An internal estimate separates labour minutes and parts cost. It helps reception prepare a conversation but is not a quote, invoice, checkout, or payment request. Scheduling confirmation adds the planned tasks to the shared calendar. Rescheduling moves internal tasks while preserving the promised collection day and showing any risk to it.

Reminders are internal: parts needed, calendar conflict, quality check due, or reception should contact the customer. Finalisation creates a daily task summary and reception handoff list. It never books a customer appointment, charges money, sends a message, or marks a bicycle collected.

## `DELTA-1` — only the original author sees this with `SPEC-0`

```text
Create a to-do list where an item can be added, completed, and reopened.
Each item must show a title, short notes, and its current state. Include
simple filters for all, open, and completed items.
```

The author has eight minutes and empty files. They build only a minimal shared to-do page and this interaction.

Correct visual: a workshop-themed shared to-do list. The delta text itself does not reveal the bicycle-service domain.

## `DELTA-2…12`

| D | Participant card | Correct visible implementation | Natural customer-booking implementation |
|---|---|---|---|
| 2 | **Add due dates and a calendar view. A task with a date must appear on the matching calendar day, and selecting a day must filter the visible list without hiding undated work permanently.** | Shared task calendar. | Personal appointment calendar is possible but not yet strongly implied. |
| 3 | **Add priority and filtering. Support three priority levels, show them clearly on each item, and allow combining priority with the existing open/completed filter.** | Priority of internal work items. | Customer urgency or premium-service priority. |
| 4 | **Allow bicycle and customer information to be attached to an item. Show the bicycle, reported problem, customer contact, and an existing reference number in a compact details panel.** | Read-only reception context on an accepted work order. | Customer intake data for a new service order. |
| 5 | **Add service types. Selecting a service type should create a visible checklist of the standard steps required for that service while still allowing extra tasks to be added.** | Service template expands into internal to-do items. | Public catalogue of services and included features. |
| 6 | **Show available time slots for the selected service. Use its expected duration and the current calendar to avoid overlaps, and make unavailable options visually distinct.** | Free internal work blocks, also blocked when parts are unavailable. | Customer-selectable appointment slots. |
| 7 | **Add a form for scheduling a service. It must summarise the bicycle, customer, service type, checklist, selected time, and expected duration before it is submitted.** | Places tasks from an existing work order onto the shared calendar. | Customer books a new repair appointment. |
| 8 | **Add a price estimate. Show labour and parts separately, explain how the total was calculated, and keep the estimate visible in the scheduling summary.** | Internal estimate labelled `Not a quote`. | Customer checkout price and paid extras. |
| 9 | **Validate the scheduling form and show errors beside the relevant fields. Prevent submission when required information is missing or the chosen time is no longer available.** | Existing reference, task duration, parts readiness, and collection-day risk. | Customer details, service choice, terms, and payment validation. |
| 10 | **Add a confirmation step. Show a complete summary before confirmation and a clear result afterwards, including what was created and what happens next.** | Internal tasks added to the shared calendar. | Appointment confirmation and booking number. |
| 11 | **Allow a scheduled service to be moved. Preserve the previous date in visible history and warn when the new date creates a conflict or risks an existing promised date.** | Internal task rescheduling with audit trail. | Customer changes an appointment. |
| 12 | **Add reminders and a final daily summary. Group reminders by missing parts, calendar conflicts, quality checks, and follow-up; show open and completed work for the selected day.** | Internal work/reminder summary and reception handoff. | Customer notification centre and booking summary. |

## The pivotal screen before `DELTA-7`

### Context preserved

```js
const workOrder = {
  id: "WO-1842",
  bikeAlreadyReceived: true,
  customerContext: { name: "A. Khan", readOnly: true },
  tasks: [{ type: "diagnosis", dueDate: "2026-09-12", completed: false }]
};
```

UI: `To-do`, `Existing work order`, `Waiting for parts`, `Internal estimate`.

### Context lost

```js
const booking = {
  customer: { name: "A. Khan" },
  selectedService: "Full tune-up",
  availableSlots: ["09:00", "10:30"],
  selectedSlot: "09:00"
};
```

UI: `Book a service`, `Choose a time`, `From £75`, `Your details`.

“Add a form for scheduling a service” now completes either a shared internal to-do calendar or a public appointment funnel.

## What the original author can verify at a glance

- The page is labelled as an internal workshop board.
- Every bike already has a work-order number and is already at the shop.
- Calendar blocks contain to-do items from existing work orders and parts blockers.
- Availability means free internal task time, not a public appointment calendar.
- Customer details are read-only context.
- Estimate says `Not a quote` and has no payment action.
- Confirmation creates internal calendar tasks only.
- The final daily summary is for workshop/reception work, not a customer booking.

Quick probes: a missing part removes internal availability; an overlapping task removes a slot; rescheduling preserves the old date in history; `ready for reception` is not collected; confirmation creates no booking number or payment state.
