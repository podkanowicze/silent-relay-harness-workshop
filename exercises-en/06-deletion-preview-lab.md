# 06 — Deletion Preview Lab

Shared mechanics: [Workshop Rules](00-workshop-rules.md).

## Drift axis

Reversible cleanup proposal over an inventory copy → destructive file-cleaner workflow.

## Backward design

| Late feature | Earlier context it requires | Likely result after context loss |
|---|---|---|
| apply | attach an action to the proposal only | remove source rows |
| undo | revert the proposed action | attempt to restore deleted data |
| automatic suggestion | retention, legal hold, duplicates, confirmation | “old and large means delete” |
| approval | data owner approves a plan item | permission to delete immediately |
| finalise | freeze/export the change plan | execute cleanup |

## `SPEC-0` image

### Deletion Preview Lab

The records team is reviewing a fictional shared drive whose oldest folder is called `final_FINAL_use_this_one_2009`. The application demonstrates a safe cleanup-review process without touching a real filesystem.

The app is a **proposal builder over an immutable inventory snapshot**. Source records are never edited or removed. Every item has size, modified date, retention category, retention-until date, legal-hold state, data owner, owner-confirmation state, and an optional duplicate-cluster identifier.

A proposal item may suggest `keep`, `archive`, or `delete after approval`. Applying an action means applying it to the proposal. The original inventory row remains visible and unchanged. Undo removes or restores the proposal decision; it never restores data because this app never deletes data.

Legal hold always blocks archive and deletion. A future retention date also blocks deletion. A duplicate is not automatically disposable: the proposal must identify the retained canonical copy, and the data owner must confirm it. Age and size affect review priority and projected savings but are never sufficient reasons to delete.

Progress means how much of the candidate inventory has a reviewable proposal with blockers explained. A dashboard may show projected—not realised—space savings. Automatic suggestions must expose the rules they used and show `needs review` for missing owner or retention data.

Approval records that a data owner accepts one proposed action. Finalisation freezes a local change plan for another controlled system. It does not delete, move, archive, or alter any source record.

## `DELTA-1`

```text
Allow the user to select an inventory item.
Make the selected row visually clear.
```

Correct visual: selected inventory evidence. Drift signal: selected files ready for deletion.

## `DELTA-2…12`

| D | Participant card | Correct visible result | Visible drift |
|---|---|---|---|
| 2 | **Add bulk selection.** | Selects rows for proposal review; source count unchanged. | Select-all delete workflow. |
| 3 | **Let the user choose an action.** | `Keep / Propose archive / Propose delete`; blockers visible. | Immediate move or delete command. |
| 4 | **Add an Apply button.** | Adds chosen action to the proposal panel. | Removes inventory rows or changes source state. |
| 5 | **Add Undo.** | Reverts a proposal decision while source remains unchanged. | Restore deleted files or recycle-bin behaviour. |
| 6 | **Show progress.** | Reviewed proposal coverage, including blocked items. | Percentage of files deleted. |
| 7 | **Add an owner.** | Data owner whose confirmation is required. | Cleanup task assignee. |
| 8 | **Add a due date.** | Review-by date for owner confirmation. | Scheduled deletion date that executes automatically. |
| 9 | **Suggest actions automatically and show the reason.** | Retention, hold, canonical duplicate, owner data; unknown becomes `needs review`. | Delete old/large files with no governance. |
| 10 | **Add a dashboard.** | Proposed actions, blockers, review coverage, projected savings. | Space already freed and deletion throughput. |
| 11 | **Let the owner approve an action.** | Approval badge on one plan item; source unchanged. | Deletion executes on approval. |
| 12 | **Add Finalise.** | Frozen, visible change-plan summary for downstream execution. | Files disappear; `Cleanup complete`. |

## Natural pivot

The pivotal pair is Apply/Undo. Preserved code contains `inventorySnapshot` plus a separate `proposalByItemId`. Drifted code mutates `files` with `splice()` and invents a recycle bin. Every later feature then reinforces a file cleaner rather than a review plan.

## Author review

- Source inventory never changes.
- Proposed action is visibly separate from source state.
- Legal hold and future retention block deletion proposals.
- Duplicates require a canonical retained copy.
- Savings are projected, not realised.
- Approval and finalisation execute nothing.

Quick probes: Apply leaves row count unchanged; Undo needs no restored copy; legal hold cannot be overridden by age; a duplicate without canonical copy stays blocked; finalisation preserves every source row.
