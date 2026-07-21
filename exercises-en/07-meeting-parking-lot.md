# 07 — Meeting Parking Lot

Shared mechanics: [Workshop Rules](00-workshop-rules.md).

## Drift axis

Topics deliberately deferred to a future conversation → project backlog and task-management dashboard.

## Backward design

| Late feature | Earlier context it requires | Likely result after context loss |
|---|---|---|
| owner | person able to explain the topic | task assignee |
| due date | target meeting or agenda slot | work deadline |
| progress | readiness for useful discussion | task completion |
| close | discussed, even without a decision | work completed |
| dashboard | agenda health and context freshness | velocity, workload, overdue tasks |

## `SPEC-0` image

### Meeting Parking Lot

The operations group has a weekly meeting where unrelated but tempting discussions regularly consume the agenda. Its sample topic is “Why the third-floor printer believes every Tuesday is Sunday”. The application preserves those topics without pretending they are project work.

This is a **meeting parking lot**, not a task tracker. A `Topic` records the question, why it was parked, the meeting it came from, context needed to discuss it, and the person who can explain that context. That person is a `context contact`, not an assignee and not responsible for solving anything.

A revisit date means the meeting or agenda slot where the group wants to discuss the topic. It is not a delivery deadline. Priority means discussion value relative to agenda cost: how much clarity the group may gain for the time required. It is not business severity.

Topic state is `parked`, `ready for agenda`, `discussed`, or `stale`. `Discussed` is a valid end state even if the group made no decision. Stale means the original context may no longer be trustworthy; it does not mean overdue work.

Progress means agenda readiness: context attached, useful question written, required attendees known, and an estimated discussion duration. It never measures implementation. Closing a topic records what happened in the conversation: decision, no decision, moved elsewhere, or no longer relevant. History is retained.

The recommended next action is preparation for a conversation, such as asking the context contact for a screenshot. Finalisation creates the next-meeting agenda packet. It does not assign tasks, promise delivery, or report team productivity.

## `DELTA-1`

```text
Allow the user to add a parked topic.
Make the new topic visibly appear in the list.
```

Correct visual: question, source meeting, and reason parked. Drift signal: task title plus “To do”.

## `DELTA-2…12`

| D | Participant card | Correct visible result | Visible drift |
|---|---|---|---|
| 2 | **Add an owner.** | Label `Context contact` with explanatory tooltip. | Assignee avatar and workload. |
| 3 | **Add priority.** | Discussion value versus agenda minutes. | High/medium/low task severity. |
| 4 | **Add a due date.** | `Target meeting` or agenda slot. | Delivery deadline. |
| 5 | **Add statuses.** | Parked, ready for agenda, discussed, stale. | To do, in progress, done. |
| 6 | **Show progress visually.** | Readiness checks: context, question, attendees, duration. | Percent work complete. |
| 7 | **Highlight items whose date has passed.** | Missed agenda slot or stale context; never work overdue. | Red overdue tasks. |
| 8 | **Allow a card to be closed.** | Close reason includes `Discussed — no decision`; history remains. | Mark resolved/completed. |
| 9 | **Merge duplicate cards.** | Preserve both source meetings and context trails under one topic. | Delete one task and its history. |
| 10 | **Add a dashboard.** | Agenda-ready topics, stale context, minutes requested, missing attendees. | Velocity, completion, assignee load. |
| 11 | **Recommend the next action.** | A preparation step for the highest-value discussion. | Implementation task assigned to owner. |
| 12 | **Add Finalise.** | Builds a visible next-meeting agenda packet. | Closes a sprint or marks all work complete. |

## Natural pivot

Generic early names—`cards`, `ownerId`, `priority`, `dueDate`—produce a familiar task schema before status and progress arrive. Preserved names—`topics`, `contextContactId`, `targetMeetingId`, `agendaReadiness`—make the same cards resolve toward meeting preparation.

## Author review

- Main object is a discussion topic.
- Owner is visibly a context contact.
- Date is a meeting slot, not a deadline.
- Progress is agenda readiness.
- Discussed without decision is valid.
- Dashboard contains no velocity or workload.
- Finalisation creates an agenda, not completed work.

Quick probes: a discussed/no-decision topic closes validly; missing screenshot reduces readiness but creates no overdue task; a past target meeting makes context stale; merging keeps both origins; finalisation assigns nobody.
