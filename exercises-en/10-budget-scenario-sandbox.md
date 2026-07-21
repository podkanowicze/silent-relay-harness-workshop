# 10 — Budget Scenario Sandbox

Shared mechanics: [Workshop Rules](00-workshop-rules.md).

## Drift axis

What-if budget scenario → authoritative accounting ledger and spending approval workflow.

## Backward design

| Late feature | Earlier context it requires | Likely result after context loss |
|---|---|---|
| apply | change one scenario assumption only | mutate approved budget |
| variance | hypothetical difference from baseline | actual overspend |
| progress | assumptions reviewed and uncertainties named | budget spent or work completed |
| approval/lock | scenario ready for discussion and immutable snapshot | financial commitment authorised |
| finalise | export comparison | post amounts to ledger |

## `SPEC-0` image

### Budget Scenario Sandbox

The Department of Sensible Umbrellas is planning next quarter. Its largest uncertain line item is “Emergency gazebo resilience”, a phrase nobody remembers approving but everybody is afraid to remove.

The application is a **what-if sandbox**, not an accounting ledger, purchasing system, or source of the approved budget. It contains an immutable baseline copied from the approved plan and any number of isolated scenarios. A scenario change never modifies the baseline or another scenario.

Each `AssumptionChange` records a line item, proposed amount, rationale, confidence range, information source, and unresolved dependency. Applying a change means applying it to the selected scenario. It does not commit money. The source person explains the assumption; they are not the owner of spending authority.

Variance means the mathematical difference between a scenario and the immutable baseline. It is not actual overspend, remaining cash, or a transaction. Negative variance may be intentional and positive variance is not automatically bad.

Progress means scenario-review coverage: material lines considered, rationales present, uncertainty ranges supplied, and dependencies named. Risk is the exposure created by uncertain assumptions and dependencies, not the probability of budget failure. Automatic suggestions may identify assumptions that deserve review but may not choose a budget.

Approval means a reviewer considers the scenario coherent enough for a planning discussion. Locking creates an immutable scenario snapshot while leaving the baseline and other scenarios untouched. Finalisation exports a side-by-side comparison with assumptions and uncertainty. It never changes an approved amount, creates a purchase, commits funds, or posts to a ledger.

## `DELTA-1`

```text
Allow the user to select a budget scenario.
Make the selected scenario visually clear.
```

Correct visual: `What-if scenario`, baseline visibly separate. Drift signal: selected active budget or fiscal period.

## `DELTA-2…12`

| D | Participant card | Correct visible result | Visible drift |
|---|---|---|---|
| 2 | **Allow a line-item amount to be changed.** | Editable scenario value beside read-only baseline. | Approved budget edited in place. |
| 3 | **Add Apply.** | Applies change to selected scenario only. | Saves authoritative budget or transaction. |
| 4 | **Add an owner.** | Label `Assumption source`; spending authority remains absent. | Cost-centre owner or approver. |
| 5 | **Add statuses.** | Draft, needs evidence, ready for review, superseded. | Open, approved, committed, spent. |
| 6 | **Show variance.** | Scenario-minus-baseline with neutral explanation. | Actual overspend/underspend alarm. |
| 7 | **Show progress.** | Review coverage of material assumptions and dependencies. | Percentage budget spent or initiative complete. |
| 8 | **Add a risk score.** | Uncertainty/dependency exposure with visible components. | Probability of financial failure or fraud. |
| 9 | **Recommend the next action.** | Assumption needing evidence or a scenario to compare. | Choose budget cuts or approve spend. |
| 10 | **Let a reviewer approve a scenario.** | `Ready for planning discussion`; no baseline change. | Financial approval or committed funds. |
| 11 | **Add Lock.** | Immutable scenario snapshot; other scenarios remain editable. | Locks authoritative ledger or fiscal period. |
| 12 | **Add Finalise.** | Export-style comparison of baseline, scenario, rationale, and uncertainty. | Posts scenario values as approved budget. |

## Natural pivot

Preserved state has `approvedBaseline`, `scenarios`, and `assumptionChanges`. Drifted state collapses these into `budget`, `lineItems`, and `saveBudget()`. Once Apply edits the baseline, variance, approval, lock, and finalise naturally become ERP controls.

## Author review

- Baseline remains visible and immutable.
- Every change belongs to one scenario.
- Source is not spending owner.
- Variance is hypothetical and neutrally styled.
- Progress is review coverage.
- Approval and lock create no commitment.
- Finalisation posts nothing.

Quick probes: applying in scenario A changes neither baseline nor B; positive variance is not automatically red; locking A leaves B editable; approval creates no committed/spent state; finalisation preserves uncertainty ranges.
