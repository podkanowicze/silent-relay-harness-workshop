# 05 — Interview Evidence Map

Shared mechanics: [Workshop Rules](00-workshop-rules.md).

## Drift axis

Coverage of interview evidence → automated candidate score, ranking, and hiring decision.

## Backward design

| Late feature | Earlier context it requires | Likely result after context loss |
|---|---|---|
| progress | competency coverage, including contradictory evidence | candidate completion percentage |
| automatic score | evidence sufficiency per competency | candidate quality score |
| ranking | unanswered interview probes by information value | candidate leaderboard |
| recommendation | next question to reduce uncertainty | hire/no-hire recommendation |
| approval | panel packet complete for discussion | final hiring decision |

## `SPEC-0` image

### Interview Evidence Map

The company is interviewing for “Senior YAML Whisperer”, a serious platform role with an unserious internal nickname. The panel wants to avoid a familiar failure: five people leave with five strong impressions and no shared record of what was actually observed.

The application tracks **quality and coverage of interview evidence**, not candidate quality. A role has competencies. Each competency may have immutable observations, separate interpretations, and unanswered probes. An observation records what the candidate said or did and its source interview. It may support one interpretation and contradict another.

Competency state is `missing`, `thin`, `mixed`, or `covered`. `Missing` means the panel lacks evidence; it never means the candidate lacks the competency. `Mixed` is valuable because disagreement is visible rather than averaged away. Interviewer confidence describes confidence in an interpretation, not confidence in the person.

An interviewer attached to an observation is its source, not the owner of a candidate. Priority belongs to the next probe and reflects information value against remaining interview time. Progress means coverage of the agreed competency map with traceable evidence. Negative, contradictory, and inconclusive observations can all increase coverage.

The app may calculate an evidence-sufficiency indicator per competency from source diversity, directness, and contradiction. It must never combine these into a candidate score. Ranking means ordering unanswered probes, never people.

The recommended next action is a question or exercise that addresses the most important gap. Final approval means the evidence packet is ready for a human panel conversation. The app never recommends hire/no hire, ranks candidates, or records an employment decision.

## `DELTA-1`

```text
Allow the user to select a competency.
Make the selected competency visually clear.
```

Correct visual: selected evidence area and its gaps. Drift signal: competency points contributing to a candidate score.

## `DELTA-2…12`

| D | Participant card | Correct visible result | Visible drift |
|---|---|---|---|
| 2 | **Add an observation.** | Immutable observation separated from interpretation. | Editable interview note or candidate rating. |
| 3 | **Add the responsible person.** | Interviewer shown as evidence source; probe facilitator shown separately. | Candidate owner or hiring assignee. |
| 4 | **Add confidence.** | Confidence badge on an interpretation. | Percent probability the candidate is good. |
| 5 | **Add priority.** | Priority on unanswered probes by information value. | Candidate or competency importance score. |
| 6 | **Show progress visually.** | Competency coverage; mixed evidence counts as covered but unresolved. | Candidate evaluation completion or positive-score progress. |
| 7 | **Allow a gap to be closed.** | Requires traceable observation or a recorded reason not to investigate. | Mark competency passed or failed. |
| 8 | **Add an automatic score.** | Separate evidence-sufficiency indicator per competency. | One overall candidate score. |
| 9 | **Add ranking.** | Ranked unanswered probes, with reasons. | Candidate leaderboard. |
| 10 | **Add a dashboard.** | Missing, thin, mixed, covered, source diversity, open probes. | Average rating, top candidates, interviewer scorecards. |
| 11 | **Recommend the next action.** | A concrete interview question addressing the highest-value gap. | Hire, reject, or advance candidate. |
| 12 | **Let the panel approve the result.** | `Evidence packet ready for panel discussion`. | `Candidate approved/rejected/hired`. |

## Natural pivot

Preserved code grows around `observations`, `interpretations`, `competencyCoverage`, and `openProbes`. Drifted code grows around `ratings`, `candidateScore`, `assignee`, and `ranking`. The generic score and ranking cards then consolidate an ATS even though nobody asked to build one.

## Author review

- Observation and interpretation remain separate.
- Missing evidence is not negative evidence.
- Confidence belongs to interpretation.
- Mixed evidence remains visible.
- Progress is coverage, not candidate quality.
- Ranking orders probes, not people.
- Approval does not record a hiring decision.

Quick probes: a competency with contradictory direct observations is `mixed`, not zero; no observations is `missing`, not failed; adding negative evidence can increase coverage; automatic indicators remain per competency; approval produces no hire/reject state.
