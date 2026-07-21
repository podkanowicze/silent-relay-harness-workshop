# 12 — Book Club Set Request

Shared mechanics: [Workshop Rules](../exercises-en/00-workshop-rules.md).

## The two recognisable products

- Intended: library staff collect group interest and request a temporary multi-copy book-club set from another branch.
- Drifted: an online bookstore selling individual copies.

Both use catalogue, minimum group size, copy availability, selection, quantity, value, group/customer details, order form, waitlist, recommendation, and confirmation.

## Backward design

| Pivotal feature | Correct meaning that must survive | Meaning after drift |
|---|---|---|
| copies | library-owned set expected to return together | retail stock |
| value | replacement value of loaned copies | unit sale price |
| order | inter-branch set request after group threshold | book purchase |
| waitlist | wait for a complete set to return | retail backorder |
| confirmation | lending branch accepts temporary transfer | paid order and delivery |

## `SPEC-0` image

### Book Club Set Request

Library branches share book-club sets containing multiple copies of one title. The catalogue includes `A Brief History of Very Long Meetings`, which is unexpectedly popular with the Tuesday group.

This application handles **inter-branch loan requests for complete book-club sets**, not book sales. A local librarian creates a group request for registered library members and a planned discussion date. No individual owns a copy.

A request needs at least eight confirmed members before it can be sent. It names one title, requesting branch, discussion date, preferred pickup date, and group contact. Members confirm interest using valid library-card references. Interest is not a purchase and does not reserve a copy.

A `BookClubSet` has lending branch, title, set ID, total copies, copies currently present, earliest available date, condition summary, replacement value per copy, and return rules. A viable request requires at least eight copies available together; it cannot assemble a hidden partial set without showing the shortfall.

Selecting a set creates a proposal and changes no availability. The lending librarian confirms the transfer. Only then do the copies become allocated to the requesting branch.

Replacement value is displayed for accountability and damage reporting. It is not a price, deposit, discount, or amount payable. Every summary shows `Amount payable here: £0`.

The requested return date is 21 days after pickup and must fall after the discussion date. A waitlist is for a complete set expected to return; it is not an individual-copy backorder. Automatic recommendation compares group size, copy count, dates, branch transfer time, set condition, and accessibility format requirements.

Final approval records an inter-branch transfer pending pickup. It creates no sale, shipment to a home address, customer order number, or ownership change.

## `DELTA-1`

```text
Create a searchable book catalogue with filters for title, author,
format, and category. Each result must have a clear cover-like visual,
summary, and visible active filters.
```

Correct visual: library-set context established by the author. Drift signal: online bookstore catalogue.

## `DELTA-2…12`

| D | Participant card | Correct visible implementation | Natural bookstore implementation |
|---|---|---|---|
| 2 | **Add group interest. Show confirmed participants for each title, progress towards a minimum of eight, and the exact state before and after the threshold is reached.** | Registered-member interest group. | Pre-order count or bulk-purchase minimum. |
| 3 | **Show copy availability. Display total copies, copies currently together, earliest available date, lending location, format, and condition without hiding partial-set shortfalls.** | Complete library-owned sets. | Retail stock by format. |
| 4 | **Allow one title and set to be selected. Highlight it, show all date and copy restrictions, and keep viable alternatives visible without changing availability.** | Proposed inter-branch set. | Product selected for purchase. |
| 5 | **Add quantity and set summary. Show copies requested, copies available together, confirmed readers, and any shortfall, and prevent the same physical set from being selected twice.** | One coordinated loan set. | Book quantity in cart. |
| 6 | **Show monetary value per copy and for the complete set. Explain what the value represents and display the amount payable by the requesting group separately.** | Replacement value; `Payable: £0`. | Unit price, subtotal, and discount. |
| 7 | **Add group details. Include requesting location, group contact, registered-member references, discussion date, preferred pickup window, required format, coordinating librarian, and planned return date.** | Library group and inter-branch transfer. | Customer, delivery, and gift details. |
| 8 | **Add a form for submitting the order. It must summarise title, set, quantities, availability, value, group, dates, pickup, return, and any shortfall before submission.** | Inter-branch loan request. | Bulk book checkout. |
| 9 | **Validate the complete order with local errors. Require eight valid members, eight available copies together, compatible dates, a return 21 days after pickup, and no unresolved format mismatch.** | Library lending rules. | Cart, stock, address, and payment validation. |
| 10 | **Add a waitlist when a complete set is unavailable. Show the expected return event, queue state, copy shortfall, and the conditions required before the request becomes viable.** | Wait for whole set to return. | Retail backorder for copies. |
| 11 | **Recommend the best set automatically. Compare member count, copies, dates, branch-transfer time, condition, and format, and explain every reason without confirming it.** | Explainable inter-branch suggestion. | Cheapest/fastest retail offer. |
| 12 | **Allow the lending librarian to approve or reject the result. Show allocated set ID, copies, branches, pickup and return dates, condition, and what approval changes.** | Temporary branch transfer. | Paid order, home delivery, or ownership transfer. |

## The pivotal screen before `DELTA-8`

### Context preserved

```js
const setRequest = {
  requestingBranchId: "BR-4",
  setId: "SET-81",
  confirmedMemberCards: 8,
  copiesRequested: 8,
  payableHere: 0
};
```

UI: `Book-club set`, `8/8 members`, `Inter-branch request`, `Return due`.

### Context lost

```js
const cart = {
  customerId: "BR-4",
  isbn: "978-…",
  quantity: 8,
  unitPrice: 9.99,
  total: 79.92
};
```

UI: `Basket`, `Quantity`, `Delivery`, `Checkout`.

## What the original author can verify at a glance

- The object is a physical library set with a set ID.
- Eight registered members and eight copies together are required.
- Selection does not change availability; librarian approval does.
- Monetary values are replacement values and payable amount is £0.
- Return date and condition remain visible.
- Approval transfers no ownership and creates no home delivery.

Quick probes: seven members cannot submit; eight scattered copies that are not one viable set cannot submit; selection changes no stock; invalid return date fails; approval creates no sale or customer order number.
