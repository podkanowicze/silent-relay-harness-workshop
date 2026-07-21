# 08 — Odd Socks Lost & Found

Shared mechanics: [Workshop Rules](00-workshop-rules.md).

## Drift axis

Staff-assisted match suggestions → marketplace listing, ownership transfer, or delivery fulfilment.

## Backward design

| Late feature | Earlier context it requires | Likely result after context loss |
|---|---|---|
| match score | public similarities separated from secret verification clues | proof of ownership from keywords |
| reserve | temporarily hide a candidate pending desk check | inventory reservation |
| success | identity clues verified in person | order fulfilled or item delivered |
| recommendation | safest next verification question | best product or buyer match |
| approval | ready for an in-person desk check | ownership transferred automatically |

## `SPEC-0` image

### Odd Socks Lost & Found

The company’s reception desk handles found objects and loss reports. Current examples include one left Croc, a conference badge belonging to “Definitely Not Finance”, and an HDMI adapter described by three separate people as haunted.

The application helps staff create **possible matches** between a found-item report and a claimant’s loss report. It is not a marketplace, inventory sale, courier system, or proof of ownership.

Found reports and loss claims remain separate records. Public matching fields include category, colour, approximate location, and date window. Each report also has a private verification clue—for example a scratch under the handle or the sticker text—that must never be displayed in public matching results or used as an exposed explanation.

A match score expresses similarity of non-secret fields. It is not confidence that the claimant owns the item. Missing information lowers match quality but is not a contradiction. Conflicting public details remain visible rather than being silently averaged.

Reception is the current custodian, not the owner. A staff member attached to a case is the verification contact, not a fulfilment assignee. Reserving a possible match hides it from competing suggestions for a short desk-check window; it does not transfer possession. Expiry returns it to the match pool.

An automatic suggestion may rank possible report pairs and list public reasons. Staff must ask at least two private-clue questions in person. A successful check means those answers matched; it still only produces `ready for desk handover`. Final approval records that verification may proceed at reception. The app never declares legal ownership, ships an item, or marks it sold.

## `DELTA-1`

```text
Allow the user to select a found-item report.
Make the selected report visually clear.
```

Correct visual: selected report and custody details. Drift signal: selected product/listing.

## `DELTA-2…12`

| D | Participant card | Correct visible result | Visible drift |
|---|---|---|---|
| 2 | **Add the responsible person.** | `Verification contact`; reception remains custodian. | Seller, owner, or fulfilment assignee. |
| 3 | **Add a match score.** | Similarity of public fields with conflicts shown. | Ownership probability or buyer affinity. |
| 4 | **Allow a match to be reserved.** | Temporary desk-check hold; no ownership change. | Stock reservation or sold state. |
| 5 | **Add an expiry time.** | Hold expiry returns pair to suggestions. | Delivery deadline or payment timeout. |
| 6 | **Show progress.** | Public match reviewed, two private clues checked, desk handover pending. | Order fulfilment percentage. |
| 7 | **Mark the check successful or unsuccessful.** | Result of private-clue verification, with answers hidden. | Transaction success/failure. |
| 8 | **Suggest matches automatically and explain them.** | Public reasons only; secret clues never exposed. | Keyword proof of ownership or product recommendations. |
| 9 | **Add priority.** | Safety/perishability and reception handling need. | Valuable-item or VIP-claim priority. |
| 10 | **Add a dashboard.** | Unmatched reports, expiring holds, checks needed, custody location. | Sales, conversion, fulfilled orders. |
| 11 | **Recommend the next action.** | Safest private verification question or desk check. | Deliver, ship, sell, or assign owner. |
| 12 | **Let staff approve the match.** | `Ready for in-person desk handover`; custody remains reception. | Ownership transferred, item delivered, order complete. |

## Natural pivot

Preserved code keeps `foundReports`, `lossClaims`, `possibleMatches`, and `verificationContact`. Drifted code collapses them into `items`, `customers`, `reservations`, and `orders`. Reserve, expiry, success, dashboard, and approval then form a complete fulfilment workflow.

## Author review

- Found reports and loss claims remain distinct.
- Private clues are never displayed as match reasons.
- Match score is similarity, not ownership confidence.
- Reception remains custodian during approval.
- Reservation is temporary and reversible.
- Final approval requires an in-person handover.

Quick probes: a perfect public match with no private check cannot be approved; expiry restores availability; failed verification keeps both reports; secret clue text never appears in explanation; approval creates no owner or delivery state.
