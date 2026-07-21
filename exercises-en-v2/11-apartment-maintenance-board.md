# 11 — Apartment Maintenance Board

Shared mechanics: [Workshop Rules](../exercises-en/00-workshop-rules.md).

## The two recognisable products

- Intended: a shared internal to-do list and calendar used after a housing repair case already exists.
- Drifted: a tenant-facing marketplace for choosing and booking a paid tradesperson.

Both use tasks, calendar, repair categories, property details, availability, scheduling form, estimate, validation, confirmation, rescheduling, reminders, and completion summary.

## Backward design

| Pivotal feature | Correct meaning that must survive | Meaning after drift |
|---|---|---|
| availability | time in the housing team’s existing work plan | customer appointment inventory |
| repair form | schedule tasks on an existing case | tenant orders a new service |
| estimate | internal labour/parts planning | contractor quote |
| confirmation | internal visit added to case calendar | paid appointment booking |
| finalise | team handoff and resident-contact reminder | service ordered or repair completed |

## `SPEC-0` image

### Apartment Maintenance Board

The housing team receives repair reports through a separate contact centre. This page begins only after a case exists. The sample case says “radiator whistles when ignored”, which remains the resident’s exact report rather than a technical diagnosis.

This application is a **shared internal to-do list and calendar**, not a tenant portal or tradesperson marketplace. Every repair has an existing case number, property, resident contact context, reported problem, target response date, access state, and safety priority.

Resident details and the original report are read-only. Staff create to-do items such as triage, access check, inspect, order parts, complete repair, safety test, and follow-up inspection. Tasks may be open, completed, reopened, filtered, prioritised, and scheduled.

An available time means the estimated task duration fits the internal calendar and prerequisites are ready. A free-looking slot is unavailable when keys are missing, resident access is unconfirmed, required parts are absent, or a safety dependency remains. It is not an appointment offered to a tenant.

Access state is `resident present`, `authorised key`, `appointment required`, or `not confirmed`. The application does not send messages; it creates a visible reminder for the contact centre when resident coordination is needed.

The internal estimate separates labour time and parts cost. It is not a customer quote, invoice, or amount payable. Emergency priority comes from safety and loss of essential service, never willingness to pay.

Scheduling confirmation adds internal tasks to the existing case. Rescheduling preserves history and flags risk to the target response date. Finalisation creates a daily work summary, unresolved blockers, safety-check list, and contact-centre handoff. It does not create a new repair order, take payment, notify a resident, or claim the repair is complete before inspection.

## `DELTA-1`

```text
Create a to-do list where an item can be added, completed, and reopened.
Each item must show a title, notes, and state. Add combinable filters for
all/open/completed and three visible priority levels.
```

Correct visual: housing-team context established by the author. The delta itself remains a generic to-do list.

## `DELTA-2…12`

| D | Participant card | Correct visible implementation | Natural service-booking implementation |
|---|---|---|---|
| 2 | **Add due dates and a calendar view. Dated items must appear on the matching day; selecting a day filters the task list while preserving access to undated work.** | Shared case-task calendar. | Appointment calendar. |
| 3 | **Add repair categories. Selecting a category should create a visible standard checklist while allowing additional tasks and notes to be added or removed.** | Internal repair-task template. | Public service catalogue. |
| 4 | **Attach property and resident information. Show address, existing reference number, original report, contact context, access state, and target response date in a compact details panel.** | Read-only existing housing case. | Tenant intake for a new order. |
| 5 | **Show available time slots for the selected repair. Use expected duration and existing calendar tasks, and visibly block options when access, parts, or safety prerequisites are unresolved.** | Internal work-plan availability. | Customer-selectable appointments. |
| 6 | **Add a form for scheduling the visit. It must summarise case, property, repair category, checklist, access, selected time, expected duration, and blockers before submission.** | Schedules tasks on an existing case. | Tenant orders a contractor visit. |
| 7 | **Add an estimate. Show labour time and parts separately, explain the calculation, and display the amount payable by the resident as a distinct value.** | Internal cost; `Resident pays here: £0`. | Contractor quote and checkout price. |
| 8 | **Validate the complete form and place errors beside relevant fields. Block unknown access, missing case reference, unresolved safety prerequisites, absent parts, or a newly conflicting time.** | Internal readiness gates. | Customer, address, service, terms, and payment validation. |
| 9 | **Add a confirmation step. Show a complete summary before confirmation and state afterwards exactly which tasks were added, which date was reserved, and what remains unresolved.** | Internal visit plan confirmed. | Paid appointment and booking number. |
| 10 | **Allow a confirmed visit to be moved. Preserve the old date in visible history and warn when the new date creates a conflict or risks the target response date.** | Auditable internal rescheduling. | Tenant changes appointment. |
| 11 | **Add reminders. Group them by missing access, missing parts, safety check, overdue internal task, and contact-centre follow-up, with a visible reason and due time.** | Internal coordination reminders. | Customer SMS/email notification centre. |
| 12 | **Add a final daily summary. Show open/completed tasks, scheduled visits, unresolved blockers, safety checks, and contact-centre handoffs without marking unfinished cases complete.** | Internal team handoff. | Repair ordered, paid, or completed for tenant. |

## The pivotal screen before `DELTA-6`

### Context preserved

```js
const repairCase = {
  caseRef: "HM-1842",
  residentContext: { readOnly: true },
  accessState: "not confirmed",
  tasks: [{ type: "inspect", completed: false }]
};
```

UI: `Existing case`, `Internal tasks`, `Access blocker`, `Contact-centre follow-up`.

### Context lost

```js
const serviceBooking = {
  customer: {},
  selectedService: "Radiator repair",
  availableSlots: ["09:00", "11:30"]
};
```

UI: `Book a repair`, `Choose a time`, `Get a quote`.

## What the original author can verify at a glance

- Every repair already has a case reference.
- Resident report and contact context are read-only.
- Availability depends on access, parts, and safety blockers.
- Estimate is internal and resident pays £0 here.
- Confirmation creates tasks, not a new repair order.
- Final summary does not claim unfinished work is complete.

Quick probes: unknown access blocks scheduling; missing part blocks slot; moving a visit retains old date; safety task cannot be hidden by completion percentage; confirmation creates no booking number or payment.
