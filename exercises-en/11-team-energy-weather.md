# 11 — Team Energy Weather

Shared mechanics: [Workshop Rules](00-workshop-rules.md).

## Drift axis

Anonymous group-level facilitation pulse → individual employee monitoring and performance scoring.

## Backward design

| Late feature | Earlier context it requires | Likely result after context loss |
|---|---|---|
| response status | whether aggregate publication threshold is met | named non-responders |
| trend | room-level snapshots with no stable identity | individual history |
| alert | group facilitation condition | employee risk flag |
| recommendation | action offered to the whole room | intervention assigned to a person |
| finalise | anonymous session summary | employee performance report |

## `SPEC-0` image

### Team Energy Weather

A workshop facilitator wants a quick signal about the room. Participants choose weather such as `Clear`, `Foggy`, `Stormy`, or the sample fixture `Sunny with a chance of merge conflicts`. The language is light; the privacy boundary is not.

The application records an **anonymous group pulse**, not employee feedback, attendance, wellbeing diagnosis, or performance data. A response contains weather, optional energy from 1–5, and an optional comment. It contains no name, email, workstation, employee ID, stable pseudonym, or other value that can connect one round to another.

The app publishes a round only after at least five responses. Before that it shows `Waiting for group threshold`, never individual responses. Comments are shuffled and displayed without timestamps precise enough to identify their author. Small groups remain hidden.

Comparing rounds means comparing aggregate snapshots for the same workshop room. The system cannot say that one person became more stormy or failed to respond. “Response status” describes whether the group threshold has been reached, not which people responded.

An alert is a facilitation signal: for example, at least 40% `Foggy/Stormy` with five or more responses. It prompts a whole-room action such as a break, recap, or anonymous question. Energy and weather remain separate; they are not combined into an employee score.

The dashboard shows distributions, group trend, threshold state, and anonymous themes. Finalisation freezes an aggregate session summary for the facilitator. It never creates personal histories, rankings, manager alerts, attendance records, or individual follow-ups.

## `DELTA-1`

```text
Add a weather response control.
Make the selected weather visually clear.
```

Correct visual: anonymous choices and no identity field. Drift signal: name, avatar, employee, or login.

## `DELTA-2…12`

| D | Participant card | Correct visible result | Visible drift |
|---|---|---|---|
| 2 | **Show how many responses were received.** | Aggregate count; data hidden below five. | List of responders/non-responders. |
| 3 | **Add optional comments.** | Shuffled anonymous comments after threshold. | Comment author, avatar, exact timestamp. |
| 4 | **Compare this round with the previous round.** | Aggregate distribution comparison only. | Person-by-person change. |
| 5 | **Add response status.** | `3/5 — waiting for group threshold` or `Published`. | Employee response checklist. |
| 6 | **Add an alert.** | Whole-room facilitation alert using published aggregate. | Flag a named person as disengaged or at risk. |
| 7 | **Add follow-up.** | Facilitator chooses a whole-room action. | Assign private intervention to an employee. |
| 8 | **Add a score.** | Keep separate group energy average and weather distribution, clearly labelled as session signals. | Personal engagement/performance score or blended leaderboard metric. |
| 9 | **Show trends.** | Room-level snapshots with no linking token. | Longitudinal employee profiles. |
| 10 | **Add a dashboard.** | Threshold state, distributions, room trend, anonymous themes. | Team-member table, rankings, manager view. |
| 11 | **Recommend the next action.** | Break, recap, slower pace, or anonymous question for everyone. | Coaching or escalation for an individual. |
| 12 | **Add Finalise.** | Frozen anonymous session summary. | Attendance/performance report with identities. |

## Natural pivot

The first identity field changes everything. Preserved data stores isolated `responses` inside aggregate `roundSnapshots`. Drifted data introduces `participantId`, `responded`, and `historyByPerson`. Every later comparison, status, alert, trend, and dashboard then rewards surveillance features.

## Author review

- No stable or direct identity exists.
- Fewer than five responses reveal no distribution or comment.
- Response status is group threshold only.
- Comparisons cannot link people across rounds.
- Alerts and follow-ups address the whole room.
- No blended personal score or ranking exists.
- Finalisation produces only an aggregate summary.

Quick probes: four responses reveal no breakdown; a fifth publishes only aggregate data; comments lack author and precise timestamp; rounds cannot answer who changed; finalisation contains no participant rows.
