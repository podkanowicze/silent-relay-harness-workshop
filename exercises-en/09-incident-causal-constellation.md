# 09 — Incident Causal Constellation

Shared mechanics: [Workshop Rules](00-workshop-rules.md).

## Drift axis

Map of competing causal explanations → root-cause ranking and blame leaderboard.

## Backward design

| Late feature | Earlier context it requires | Likely result after context loss |
|---|---|---|
| confidence | support for an explanation, including contradictions | probability of guilt |
| owner | source or investigator for evidence | person responsible for incident |
| progress | uncertainty reduced across the graph | percentage of root-cause work complete |
| ranking | experiments by information value | suspects or causes by blame |
| finalise | preserve multiple explanations and unknowns | announce one culprit and close incident |

## `SPEC-0` image

### Incident Causal Constellation

The identity service failed intermittently whenever someone ordered decaf from the lobby coffee machine. Nobody believes the coffee directly controls OAuth, but the coincidence is useful because it forces the team to separate observation from explanation.

The application is a **multi-causal investigation map**, not a root-cause form or accountability tracker. A `CandidateExplanation` is falsifiable and may be `untested`, `testing`, `supported`, or `contradicted`. Supported does not mean proven root cause.

`Evidence` is an immutable observation with source and time. The same evidence may support one explanation, contradict another, and be irrelevant to a third. It remains visible after an explanation is contradicted. A person attached to evidence is its information source or the investigator running an experiment—not the owner of a cause and never the person to blame.

Confidence describes how well the current evidence supports one explanation. Contradictory evidence must remain visible beside supporting evidence. Weight means strength of one evidence-to-explanation link, not percentage contribution to the incident; weights need not sum to 100.

Priority belongs to the next experiment and reflects information value versus effort. Progress means reduction of uncertainty: explanations tested, relationships evidenced, contradictions surfaced, and gaps named. A negative experiment may increase progress.

Ranking means ordering proposed experiments, not causal explanations or people. The recommended next action is the experiment most likely to distinguish competing explanations. Finalisation produces a summary of what is known, unknown, supported, and contradicted. It never announces blame, assigns percentages of fault, or claims that one root cause has been proven.

## `DELTA-1`

```text
Allow the user to select a candidate explanation.
Make the selected explanation visually clear.
```

Correct visual: selected node with supporting and contradicting evidence. Drift signal: selected culprit or root cause.

## `DELTA-2…12`

| D | Participant card | Correct visible result | Visible drift |
|---|---|---|---|
| 2 | **Add evidence.** | Immutable observation linked separately as support or contradiction. | Editable justification attached to a cause. |
| 3 | **Add the responsible person.** | Evidence source and experiment investigator shown as distinct roles. | Cause owner, accountable team, or blamed person. |
| 4 | **Add confidence.** | Evidence-balance badge with `insufficient evidence`. | Probability that this is the root cause. |
| 5 | **Add weight.** | Strength on each evidence relationship; no total of 100%. | Percentage contribution or blame. |
| 6 | **Add statuses.** | Untested, testing, supported, contradicted. | Open, responsible, resolved. |
| 7 | **Show progress.** | Tested explanations, mapped contradictions, named gaps. | Percentage until root cause is found. |
| 8 | **Mark an experiment successful or unsuccessful.** | Whether it produced distinguishing evidence; a negative result may succeed. | Success means explanation true. |
| 9 | **Add ranking.** | Experiments ranked by information value/effort. | Causes or people ranked by likelihood/blame. |
| 10 | **Merge duplicates.** | Equivalent explanations linked while all evidence relations survive. | Delete one cause and its contradictory history. |
| 11 | **Recommend the next action.** | Best discriminating experiment, with competing explanations named. | Fix the highest-ranked cause or contact its owner. |
| 12 | **Add Finalise.** | Summary preserves supported, contradicted, and unknown paths. | `Root cause confirmed`, culprit, 100% complete. |

## Natural pivot

The word “responsible” is the first pressure point. Preserved code uses `evidenceSourceId`, `investigatorId`, and `relationshipStrength`. Drifted code uses `ownerId`, `causeProbability`, and `faultPercent`. Ranking and finalisation then turn uncertainty into a polished blame report.

## Author review

- Evidence is immutable and reusable across explanations.
- Supporting and contradicting evidence are both visible.
- People are sources/investigators, never cause owners.
- Weights do not represent percentage contribution.
- Negative experiments can increase progress.
- Ranking orders experiments.
- Finalisation retains multiple explanations and unknowns.

Quick probes: relationship weights may total above 100; contradicted explanations keep history; a negative discriminating experiment is successful evidence; missing evidence does not produce 0% guilt; finalisation names no culprit.
