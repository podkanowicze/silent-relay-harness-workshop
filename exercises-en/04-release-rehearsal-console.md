# 04 — Release Rehearsal Console

Shared mechanics: [Workshop Rules](00-workshop-rules.md).

## Drift axis

Scripted release rehearsal → production deployment controller.

## Backward design

| Late feature | Earlier context it requires | Likely result after context loss |
|---|---|---|
| success/failure | quality of evidence from a simulated step | deployment result |
| retry | replay the scripted observation without side effects | redeploy production |
| risk | unresolved rehearsal assumptions | live release failure probability |
| approval | rehearsal packet complete for human review | authorisation to deploy |
| finalise | freeze and export rehearsal evidence | execute or mark release complete |

## `SPEC-0` image

### Release Rehearsal Console

The platform team rehearses changes before a real release. The sample scenario is `billing-api 4.2`, whose most alarming scripted observation is “the invoice PDF briefly speaks fluent Latin”. The joke is in the fixture; the tool itself is an internal engineering control.

This application is a **local simulation and evidence recorder**, not a deployment system. It has no network and never changes an environment. A rehearsal scenario contains ordered steps, an expected observation, a scripted simulated observation, a rollback trigger, and questions for the review.

“Run” reveals the next scripted observation and advances only the local rehearsal clock. Environment labels such as `staging` and `production` describe the scenario being practised; they are not connected targets. The actor is the person performing a rehearsal role, not the owner of a production service.

A step succeeds when it produces useful evidence against its prediction. A surprising or negative observation may therefore be a successful rehearsal step. Step failure means evidence could not be collected. Progress is coverage of planned steps, rollback branches, and unanswered questions—not percentage of a deployment completed.

Risk represents unresolved rehearsal assumptions and missing rollback evidence. The console may recommend the next simulation step with the greatest information value. Retrying resets only that step’s simulated observation and preserves its history.

Approval means the rehearsal packet is complete enough to discuss at the real release review. Finalisation freezes the local report: observations, missing evidence, rollback gaps, and open questions. It never deploys, rolls back, promotes, or authorises production work.

## `DELTA-1`

```text
Allow the user to select a rehearsal scenario.
Make the selected scenario visually clear.
```

Correct visual: `Selected rehearsal`. Drift signal: selected environment or release target.

## `DELTA-2…12`

| D | Participant card | Correct visible result | Visible drift |
|---|---|---|---|
| 2 | **Add a Run button.** | Reveals one scripted observation; label says `Run simulation step`. | `Deploy`, live console, environment mutation. |
| 3 | **Add a status to every step.** | Not run, evidence captured, evidence missing. | Pending, deploying, deployed, failed. |
| 4 | **Add an owner.** | Rehearsal actor and role. | Production service owner or deploy assignee. |
| 5 | **Add a timer.** | Local rehearsal duration and time-box warning. | Release ETA or deployment timeout. |
| 6 | **Mark a step successful or unsuccessful.** | Whether useful evidence was collected; negative observations can succeed. | Healthy production result equals success. |
| 7 | **Show progress visually.** | Coverage of steps, rollback branches, and questions. | Percentage deployed. |
| 8 | **Calculate a risk indicator.** | Missing predictions, rollback evidence, and unanswered questions. | Probability production will fail. |
| 9 | **Allow a failed step to be retried.** | Replay simulation; previous attempt remains visible. | Redeploy or rerun against an environment. |
| 10 | **Add a summary dashboard.** | Evidence captured, gaps, surprising observations, branches rehearsed. | Live release health and environment status. |
| 11 | **Let a reviewer approve the result.** | `Rehearsal packet ready for release review`. | `Approved for production deployment`. |
| 12 | **Add a finalise action.** | Frozen local report with open questions retained. | Deploy now, promote, rollback, or `Release complete`. |

## Natural pivot

After early drift, code contains `selectedEnvironment`, `deploy()`, `deploymentStatus`, and `serviceOwner`. The same later cards become a textbook deployment dashboard. Preserved code contains `selectedScenarioId`, `revealObservation()`, `evidenceStatus`, and `rehearsalActor`.

## Author review

- Environment names are scenario labels only.
- Run reveals scripted local data.
- Negative observations can still produce successful evidence.
- Progress measures rehearsal coverage.
- Retry preserves previous attempts.
- Approval and finalisation never authorise or execute deployment.

Quick probes: running changes no external target; a rollback-trigger observation can be evidence success; retry retains attempt one; 100% step execution with an unanswered rollback question is not complete; finalisation keeps open questions visible.
