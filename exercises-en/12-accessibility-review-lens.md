# 12 — Accessibility Review Lens

Shared mechanics: [Workshop Rules](00-workshop-rules.md).

## Drift axis

Evidence aid for a human accessibility review → automated compliance score and legal certificate.

## Backward design

| Late feature | Earlier context it requires | Likely result after context loss |
|---|---|---|
| progress | review coverage of interaction types | percentage compliant |
| automatic check | local detection with inconclusive state | authoritative rule verdict |
| score | completeness of evidence | accessibility conformance score |
| pass/fail | execution result of one check | whole product legally passes/fails |
| approval | review packet ready for specialist review | compliance certification |

## `SPEC-0` image

### Accessibility Review Lens

The design-system team reviews fictional prototype screens before specialist testing. The sample screen contains a button labelled “Click here, probably”, which is funny only because it is deliberately bad test data.

The application is an **evidence organiser for an internal accessibility review**, not a compliance scanner, legal opinion, or certification tool. A `Screen` contains interaction types to review: keyboard, focus order, labels, contrast, zoom/reflow, error handling, and announcements.

An `Observation` records what a reviewer actually tested, the method, the visible result, affected interaction, and supporting evidence. A separate `Interpretation` may describe a possible barrier and severity. The reviewer is the source of evidence, not the owner of a legal verdict. Severity describes likely user impact, not litigation risk.

State is `not reviewed`, `evidence captured`, `needs specialist`, or `ready for specialist review`. Unknown and not reviewed never mean pass. Progress means interaction-type coverage with traceable evidence; negative findings and inconclusive tests can increase coverage.

Automatic checks are small local heuristics over the prototype fixture—for example missing visible label text or insufficient sample contrast. Each result is `detected`, `not detected`, or `inconclusive`, and shows exactly what was inspected. “Not detected” is not proof that a barrier is absent.

Any score is an evidence-completeness score per interaction type, never a conformance percentage. Pass/fail applies only to whether one automatic check executed against its stated condition. The recommended next action is a manual test that fills the most important evidence gap. Approval means the evidence packet is ready for an accessibility specialist. Finalisation never displays “compliant”, issues a certificate, or replaces human and legal assessment.

## `DELTA-1`

```text
Allow the user to select a prototype screen.
Make the selected screen visually clear.
```

Correct visual: selected review target and interaction coverage. Drift signal: selected product awaiting certification.

## `DELTA-2…12`

| D | Participant card | Correct visible result | Visible drift |
|---|---|---|---|
| 2 | **Add an observation.** | Test method and observed result separated from interpretation. | Unexplained compliance issue checkbox. |
| 3 | **Add the responsible person.** | Label `Evidence reviewer/source`. | Compliance owner or person liable. |
| 4 | **Add severity.** | Likely user impact on an interpreted barrier. | Legal/business risk score. |
| 5 | **Add confidence.** | Confidence in the interpretation, not in product compliance. | Probability the product passes. |
| 6 | **Show progress.** | Interaction-type evidence coverage; unknown remains incomplete. | Percentage accessible/compliant. |
| 7 | **Add an automatic check.** | Local heuristic with inspected condition and inconclusive state. | Black-box compliance scanner. |
| 8 | **Add a score.** | Evidence completeness per interaction type. | One accessibility grade. |
| 9 | **Add pass/fail.** | Whether each local check executed against its narrow condition. | Whole screen or product passes/fails accessibility. |
| 10 | **Add a dashboard.** | Coverage gaps, observations, inconclusive checks, specialist needs. | Compliance percentage and certified screens. |
| 11 | **Recommend the next action.** | A concrete manual test for the highest-value gap. | Declare remediation, legal approval, or automatic fix. |
| 12 | **Let a reviewer approve the result.** | `Evidence packet ready for specialist review`. | `WCAG compliant`, certificate, or legal sign-off. |

## Natural pivot

Preserved code contains `observations`, `interpretations`, `interactionCoverage`, and `checkExecutionResult`. Drifted code introduces `violations`, `complianceScore`, `screenPass`, and `certified`. The score and pass/fail cards make the second model look polished while erasing unknowns.

## Author review

- Observation and interpretation remain distinct.
- Unknown and not reviewed never appear as pass.
- Severity is user impact, not legal risk.
- Progress and scores describe evidence completeness.
- Automatic checks expose narrow conditions and inconclusive results.
- Pass/fail belongs only to individual check execution.
- Approval hands evidence to a specialist; no certificate exists.

Quick probes: an unreviewed interaction lowers coverage but is not failed; “not detected” does not mark compliant; an inconclusive check remains visible; negative findings can increase coverage; approval never creates `compliant/certified` UI.
