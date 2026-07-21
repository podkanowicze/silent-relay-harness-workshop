# 03 — Safe Plate Queue

Shared mechanics: [Workshop Rules](00-workshop-rules.md).

## Drift axis

Workplace allergy-accommodation triage → food ordering, popularity ranking, or unsafe automatic approval.

## Backward design

| Late feature | Earlier context it requires | Likely result after context loss |
|---|---|---|
| automatic check | structured allergen and kitchen-isolation data | keyword scan or recommendation score |
| priority | medical handling urgency, never popularity | VIP or high-value order priority |
| total indicator | safety gates kept separate from preferences | one blended customer score |
| eligibility | every allergen must have a safe preparation path | popular dish or high score passes |
| approval | kitchen confirms an accommodation plan | paid order confirmation |

## `SPEC-0` image

### Safe Plate Queue

The company cafeteria runs “Experimental Thursday”, a weekly menu whose names are more adventurous than the finance department. The current dishes are Spreadsheet Curry, Quarterly Beetroot, and Pasta al Dente but Emotionally Available.

The application handles **meal-accommodation requests**, not food purchases. An employee indicates a preferred dish, but the kitchen decides whether it can prepare a safe variant. There is no payment, basket, rating, loyalty level, or promise that a preferred dish will be served.

A request separates medically relevant allergens from preferences. Allergens use structured choices: nuts, gluten, dairy, egg, and sesame, plus severity `avoid`, `cross-contact unsafe`, or `emergency plan`. Free text provides handling context but never creates or removes an allergen. Preferences such as “no coriander” are visible to the kitchen but never raise safety priority. Accessibility and religious dietary requirements are displayed separately and are never treated as allergies.

Each dish declares ingredients and a required preparation station. The kitchen has Green, Blue, and Purple stations with explicit allergen exclusions. A request is feasible only if every declared allergen is excluded by both the dish variant and its assigned station. Unknown station data is not safe. Staff may choose another dish or station, but must explain the change.

Priority is based on the severity of safe handling and how soon the pickup window begins, not order value or popularity. An automatic check may show which allergens passed or failed against the dish and station. It is advice for a kitchen safety officer, never an automatic medical decision. Approval means “safe preparation plan accepted”; it does not place an order, charge an employee, or claim that food has been prepared.

## `DELTA-1`

```text
Allow the user to indicate a preferred dish.
Make the preference visually obvious.
```

Correct visual: `Preference — kitchen will confirm`. Drift signal: `Add to order`, price, quantity, or guaranteed selection.

## `DELTA-2…12`

| D | Participant card | Correct visible result | Visible drift |
|---|---|---|---|
| 2 | **Add dietary details.** | Separate allergen, severity, preference, religious need, and accessibility sections. | One free-text “special instructions” box. |
| 3 | **Add a pickup window.** | Requested service window used for triage, not a reservation slot. | Delivery time or booked collection slot. |
| 4 | **Add a form for submitting a request.** | Accommodation request with dish preference and safety data. | Restaurant order with quantity, extras, and payment. |
| 5 | **Validate the request.** | Structured allergen/severity required; unknown station blocks safe status. | Only address, contact, and cart validation. |
| 6 | **Add a visible priority.** | Safety urgency and pickup proximity, with explanation. | VIP, spend, popularity, or first-come order priority. |
| 7 | **Let kitchen staff score readiness from 1 to 10.** | Readiness of the proposed preparation plan, not the employee. | Dish rating, customer value, or allergy severity score. |
| 8 | **Suggest the check automatically and show what passed.** | Allergen-by-dish and allergen-by-station chips; unknown visibly fails. | Keyword score or unexplained green badge. |
| 9 | **Add a popularity indicator for dishes.** | Informational only and visually outside the safety decision. | Popularity increases priority or overrides safety. |
| 10 | **Show one overall summary.** | Separate panels: safety gates, staff readiness, preference, popularity. | One blended score that hides failed allergens. |
| 11 | **Highlight requests ready to proceed.** | Every allergen has a safe dish and station, confirmed by staff. | High score or popular dish qualifies. |
| 12 | **Let kitchen staff approve the result.** | `Safe preparation plan accepted`; no order or prepared-food state. | `Order confirmed`, charged, queued, or “meal prepared”. |

## Natural pivot

The form card is pivotal. Preserved code has `accommodationRequest`, `allergens`, `severity`, `preferredDishId`, and `stationExclusions`. Drifted code has `order`, `menuItemId`, `quantity`, `pickupTime`, and `specialInstructions`. Later “automatic check” will validate food safety in the first model and order completeness in the second.

## Author review

- Preference is not a guaranteed order.
- Allergies are structured and separate from preferences.
- Dish and preparation station are both checked.
- Unknown is visibly unsafe, not neutral.
- Popularity never changes safety or priority.
- Approval accepts a preparation plan only.

Quick probes: a nut-safe dish at a station with unknown nut controls fails; “no coriander” does not raise priority; popularity cannot override gluten failure; changing dish requires a reason; approval creates no payment or prepared state.
