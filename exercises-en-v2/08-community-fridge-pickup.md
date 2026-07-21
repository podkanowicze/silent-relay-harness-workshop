# 08 — Community Fridge Pickup

Shared mechanics: [Workshop Rules](../exercises-en/00-workshop-rules.md).

## The two recognisable products

- Intended: a free allocation and pickup page for donated surplus food.
- Drifted: a grocery e-commerce checkout.

Both products use product cards, quantities, expiry, basket, value, pickup slots, household details, order form, substitutions, allocation, and confirmation.

## Backward design

| Pivotal feature | Correct meaning that must survive | Meaning after drift |
|---|---|---|
| stock | donated units awaiting fair allocation | grocery inventory for sale |
| value | estimated rescued-food value for reporting | sale price |
| basket/order | request subject to household limits and volunteer allocation | purchased groceries |
| pickup slot | safe collection window for allocated food | commercial collection booking |
| confirmation | volunteer allocates items; unclaimed food returns | paid order ready for collection |

## `SPEC-0` image

### Community Fridge Pickup

Local shops donate safe surplus food to the community fridge. Today’s list includes twelve yoghurts, six loaves, and one box labelled only “excellent courgettes”, which volunteers have inspected and accepted as produce rather than a threat.

This application supports **free, fair allocation of donated food**, not grocery sales. Every item has category, quantity, use-by date, storage type, allergen information, estimated retail value, and pickup location. Users never pay.

A household may request at most six units in total and at most two units of the same item. One loaf counts as one unit; a six-pack donated as one item counts as one unit. These limits apply before allocation. Selecting items does not reduce available quantity because multiple pending requests may exist.

Use-by warnings are visible. Chilled and frozen items require a pickup window within two hours of allocation. Allergen information is displayed exactly as donated and must never be inferred from household preferences. Accessibility needs affect pickup-slot suitability but not allocation priority.

Estimated retail value is used only to report rescued-food value. Every summary must show `Amount payable: £0`; there is no payment method, discount, delivery fee, or loyalty account.

A volunteer allocates units from pending requests using household limits, item availability, expiry urgency, and pickup suitability. The system may suggest substitutions within the same food category, but the household must accept them. It never substitutes an item with incompatible allergens.

Confirmation creates a time-limited pickup allocation. Quantity is reduced only then. If the pickup window expires unclaimed, the units return to availability. Final confirmation does not represent a purchase, delivery, or ownership before collection.

## `DELTA-1`

```text
Create a browsable list of food items with search and category filters.
Each card must show a clear name, image-like visual placeholder, category,
and storage type, while keeping active filters visible.
```

Correct visual: donated-food context established by the author. Drift signal: grocery storefront.

## `DELTA-2…12`

| D | Participant card | Correct visible implementation | Natural grocery implementation |
|---|---|---|---|
| 2 | **Add quantity and expiry information to every item. Highlight low quantity and near-expiry items without hiding allergen or chilled/frozen storage information.** | Donated units and safety urgency. | Retail stock and promotional urgency. |
| 3 | **Allow the user to choose quantities for multiple items. Keep the catalogue visible, prevent requesting more than currently listed, and show selection state on every affected card.** | Pending request only; stock unchanged. | Add grocery quantities to cart. |
| 4 | **Add a basket-style summary. Group selected food by storage type, show units and expiry, allow quantity edits and removal, and display any household-limit warnings.** | Free allocation request. | Shopping basket. |
| 5 | **Show estimated monetary value for each selected item and the total. Display the amount payable by the household separately and explain why the two values differ.** | Rescued retail value; `Payable: £0`. | Prices, discount, and checkout total. |
| 6 | **Add pickup slots. Show location, start/end time, chilled/frozen suitability, accessibility, and remaining collection capacity, and allow one compatible slot to be selected.** | Safe community collection window. | Click-and-collect booking. |
| 7 | **Add household details. Include household reference, contact information, household size, accessibility needs, preferred pickup contact method, and explicit acknowledgement of the visible allergen information.** | Household allocation context. | Customer account and delivery contact. |
| 8 | **Add a form for submitting the order. It must summarise food, quantities, expiry, allergens, value, amount payable, household, and pickup slot before submission.** | Pending free-food request. | Grocery checkout. |
| 9 | **Validate the complete order. Enforce six total units, two of one item, available quantity, compatible pickup storage, required household details, and visible local errors.** | Fair-allocation and safety rules. | Cart, stock, contact, and payment validation. |
| 10 | **Add substitutions and waiting state. Suggest only same-category allergen-compatible replacements, require acceptance, and explain when a request must wait for volunteer allocation.** | Safe substitute in pending request. | Retail substitution and backorder. |
| 11 | **Suggest an allocation automatically. Consider household limits, current units, expiry urgency, accepted substitutions, storage, and pickup compatibility, and show every reason.** | Volunteer decision aid; no stock change yet. | Automatic order fulfilment. |
| 12 | **Allow a volunteer to confirm or reject the result. Show allocated quantities, pickup deadline, returned/unavailable items, and what happens if the allocation is not collected.** | Time-limited free pickup; stock changes now. | Paid order confirmation and collection receipt. |

## The pivotal screen before `DELTA-8`

### Context preserved

```js
const request = {
  householdRef: "HH-42",
  requestedUnits: [{ donationId: "D-19", quantity: 2 }],
  estimatedRetailValue: 7.2,
  payable: 0,
  status: "pending allocation"
};
```

UI: `Donated food`, `Household limit`, `Pending volunteer allocation`, `£0 payable`.

### Context lost

```js
const cart = {
  customerId: "HH-42",
  items: [{ productId: "D-19", quantity: 2, price: 3.6 }],
  total: 7.2
};
```

UI: `Basket`, `Subtotal`, `Choose pickup`, `Checkout`.

## What the original author can verify at a glance

- Food is explicitly donated and always free.
- Selection does not reduce quantity; volunteer confirmation does.
- Six-total/two-same household limits are visible.
- Expiry, storage, and allergens remain prominent.
- Substitutions require acceptance and allergen compatibility.
- Unclaimed allocations return to availability.

Quick probes: selecting two units leaves stock unchanged; requesting seven total units fails; incompatible frozen slot fails; allergen-conflicting substitute never appears; expired pickup restores units; confirmation creates no payment.
