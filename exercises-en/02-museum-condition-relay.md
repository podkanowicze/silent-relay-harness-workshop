# 02 — Museum Condition Relay

Shared mechanics: [Workshop Rules](00-workshop-rules.md).

## Drift axis

Append-only evidence about an artefact at custody handoffs → parcel tracking and delivery completion.

## Backward design

| Late feature | Earlier context it requires | Likely result after context loss |
|---|---|---|
| progress | required condition zones inspected | percentage of a delivery route completed |
| overdue | condition check due after custody change | late shipment |
| success/failure | handoff produced usable evidence | package delivered or failed |
| next action | inspect the most uncertain condition zone | move or dispatch the object |
| approval | next custodian acknowledges a snapshot | ownership transfer or proof of delivery |

## `SPEC-0` image

### Museum Condition Relay

The regional museum shares fragile objects with three small partner museums. The application records what each object looked like whenever custody changed. Its first sample is a Victorian moustache cup with a suspicious raspberry mark; the registrar insists that “suspicious” is a condition term, not a curatorial opinion.

This is a **condition-evidence relay**, not shipping software. An `Artifact` has stable identity. A `ConditionSnapshot` is an immutable observation made at one handoff, with time, place, observer, photographs represented by local thumbnails, and findings for the required zones: surface, structure, attachments, and packaging. Later observations never overwrite earlier ones.

A `CustodyHandoff` names the previous and next custodian. The observer is a witness to condition, not the artefact’s owner or a task assignee. “Arrived” only means the next inspection may begin. It does not mean undamaged, complete, or delivered successfully.

Each zone is `unchanged`, `new concern`, `worse`, or `not inspected`. Unknown is not healthy. Progress means required zones with usable observations. A handoff becomes `evidence complete` only when all zones are inspected or a reason for omission is recorded. A due time indicates when the post-transfer condition check should happen, not when a parcel should arrive.

The system may recommend the next zone to inspect based on missing evidence and prior concerns. It never recommends transport, modifies a courier state, or claims a cause of damage. Final staff approval means the next custodian accepts the snapshot as an accurate record for the relay. It does not transfer legal ownership and is not proof of delivery.

## `DELTA-1`

```text
Let the user select an artefact and make the selected card visually clear.
```

Correct visual: selected evidence file and latest snapshot. Drift signal: selected parcel, order, or shipment.

## `DELTA-2…12`

| D | Participant card | Correct visible result | Visible drift |
|---|---|---|---|
| 2 | **Show the current location.** | Custody location plus timestamp of latest snapshot. | Live shipment location or route animation. |
| 3 | **Add the responsible person.** | Current custodian and condition observer shown as different roles. | One `owner/assignee` for the parcel. |
| 4 | **Add a status.** | Zone evidence states and handoff evidence state. | `Shipped / In transit / Delivered`. |
| 5 | **Add a due date.** | Due time for the next condition inspection. | Delivery ETA. |
| 6 | **Show progress visually.** | Four-zone inspection coverage, with unknown visibly incomplete. | Route or delivery percentage. |
| 7 | **Highlight overdue items.** | Custody changes lacking a timely condition check. | Late shipments. |
| 8 | **Let staff mark the handoff successful or unsuccessful.** | Whether the handoff produced usable evidence, with reason. | Delivered/failed package. |
| 9 | **Allow duplicate records to be merged.** | Link duplicate artefact identities while preserving every snapshot. | Delete one shipment and its history. |
| 10 | **Add a summary dashboard.** | Missing zones, new concerns, late inspections, complete evidence sets. | In transit, delivered, late, courier performance. |
| 11 | **Recommend the next action.** | Inspect the highest-risk missing zone and explain why. | Dispatch, reroute, or contact courier. |
| 12 | **Let the receiving person approve the handoff.** | `Snapshot acknowledged by next custodian`; history remains visible. | Proof of delivery or ownership transfer. |

## Natural pivot

The decisive early fork is naming. Preserved state contains `conditionSnapshots`, `requiredZones`, `observerId`, and `nextCustodianId`. Drifted state contains `shipment`, `currentLocation`, `ownerId`, and `deliveryStatus`. By the due-date and progress cards, a polished parcel tracker is easier to extend than an evidence relay.

## Author review

- Historical snapshots are immutable and visible.
- Observer, custodian, and owner are not conflated.
- Unknown zones do not count as healthy or complete.
- Due means inspection due, not arrival ETA.
- Progress is condition coverage.
- Approval acknowledges evidence, not delivery or ownership.

Quick probes: an arrived object with an uninspected attachment is incomplete; a new concern preserves the previous snapshot; merging duplicates retains both histories; approval never changes location; late means no timely post-transfer inspection.
