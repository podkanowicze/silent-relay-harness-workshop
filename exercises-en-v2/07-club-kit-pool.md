# 07 — Club Kit Pool

Shared mechanics: [Workshop Rules](../exercises-en/00-workshop-rules.md).

## The two recognisable products

- Intended: an internal sports-club page that temporarily allocates club-owned kit to registered players.
- Drifted: an online sportswear shop.

Both products use a catalogue, variants, stock, selection, basket, value, player/customer details, order form, substitutions, recommendations, and confirmation.

## Backward design

| Pivotal feature | Correct meaning that must survive | Meaning after drift |
|---|---|---|
| stock | club assets available for temporary allocation | retail inventory |
| value | replacement value retained by the club | sale price |
| order | request for an issued kit set | customer purchase |
| unavailable item | approved temporary substitute | backorder or upsell |
| approval | kit manager records issue and return obligation | paid order fulfilment |

## `SPEC-0` image

### Club Kit Pool

The athletics club owns reusable match kit for registered players. One jacket is still recorded as “navy, probably”, a description the kit manager intends to fix after the next inventory count.

This application handles **temporary allocation of club-owned kit**, not retail sales. Every player is already registered and belongs to one team and tournament. Items remain club property and must be returned after the allocation period.

Each physical item has an asset tag, category, size, colour, condition, replacement value, and state: `available`, `provisionally selected`, `issued`, `laundry`, `repair`, or `retired`. Stock means count of physical club assets currently available. Selecting an item does not consume it; issue approval does.

Each tournament defines a mandatory kit set—for example one match shirt, one pair of shorts, one jacket, and optional goalkeeper items. A request must contain exactly the required categories, compatible sizes, registered player, team, event, issue date, return due date, and acknowledgement of current condition.

Replacement value is displayed for accountability but is not a price, deposit, amount due, or payment request. The player pays nothing in this application.

If the preferred size is unavailable, the app may suggest an approved club substitute based on the tournament rules and size chart. It must not silently change size or category. A waitlist is for a specific physical asset expected to return; it is not a retail backorder.

The kit manager approves issue only after verifying the player, required set, condition, availability, and return date. Approval changes assets to `issued` and records who must return them. It does not transfer ownership, create delivery, or generate a sales receipt.

## `DELTA-1`

```text
Create a browsable catalogue with search and filters for category,
size, and colour. Each result must have a clear visual card and the
active filters must remain visible and removable.
```

Correct visual: club-kit ownership context established by the author. Drift signal: standard sportswear storefront.

## `DELTA-2…12`

| D | Participant card | Correct visible implementation | Natural webshop implementation |
|---|---|---|---|
| 2 | **Add variants and stock information. Show category, size, colour, condition, and available quantity, and clearly disable variants that cannot currently be selected.** | Counts of club-owned physical assets. | Retail size/colour inventory. |
| 3 | **Allow items to be selected and removed. Preserve the chosen variant, show selection state on each card, and prevent the same physical item from being selected twice.** | Provisional kit allocation. | Add/remove product from cart. |
| 4 | **Add a basket-style summary. Group selected items by category, show quantities and variants, highlight missing required categories, and allow returning to the catalogue.** | Proposed mandatory kit set. | Shopping cart. |
| 5 | **Show a monetary value for every selected item and a total. Explain what the value represents and display the amount the user must pay separately.** | Replacement values; `Payable here: £0`. | Product prices and checkout total. |
| 6 | **Add player details. Include registered-player identifier, name, team, event, issue date, expected return date, and responsible coach in a compact review panel.** | Existing club player and temporary period. | Customer, delivery, or billing details. |
| 7 | **Add a form for submitting the order. It must summarise player, event, selected variants, required-set coverage, dates, condition, and value before submission.** | Requests a temporary issue. | Purchases sportswear. |
| 8 | **Validate the complete order. Block missing mandatory categories, duplicate physical assets, incompatible variants, invalid dates, unavailable stock, or an unregistered player, with local errors.** | Tournament kit-set rules. | Cart, address, payment, and stock validation. |
| 9 | **Handle unavailable items. Show an approved substitute when one exists, explain every difference, require explicit acceptance, and otherwise offer a waitlist for the original item.** | Temporary substitution or asset-return waitlist. | Backorder, alternative product, or upsell. |
| 10 | **Recommend the best complete set automatically. Use required categories, player sizing, event rules, item condition, availability, and return date, and show the reasons.** | Club-compliant allocation suggestion. | Recommended products and cross-sell. |
| 11 | **Add return information. Show due date, issued condition, items outstanding, and the states that follow return, such as laundry, repair, or available.** | Asset lifecycle and club ownership. | Returns/refunds policy. |
| 12 | **Allow the kit manager to approve or reject the result. Show which physical asset tags were issued, their condition, the responsible player, and the return obligation.** | Temporary allocation recorded. | Order paid, shipped, or ownership transferred. |

## The pivotal screen before `DELTA-7`

### Context preserved

```js
const allocation = {
  registeredPlayerId: "P-118",
  tournamentId: "T-9",
  selectedAssetTags: ["KIT-204", "KIT-311"],
  payableHere: 0,
  returnDue: "2026-10-02"
};
```

UI: `Club assets`, `Mandatory set`, `Replacement value`, `Return due`.

### Context lost

```js
const cart = {
  customerId: "P-118",
  items: [{ sku: "SHIRT-M-NAVY", quantity: 1, price: 48 }],
  total: 48
};
```

UI: `Your basket`, `Subtotal`, `Checkout`.

## What the original author can verify at a glance

- Physical asset tags are visible.
- Selection does not reduce stock; issue approval does.
- Mandatory kit-set gaps are shown.
- Monetary values are replacement values and payable amount is £0.
- Every issued item has condition and return date.
- Approval transfers no ownership and creates no delivery.

Quick probes: selecting an asset leaves it available to others until approval; one tag cannot appear twice; missing mandatory shorts blocks issue; substitute requires acceptance; approval creates no receipt or shipment.
