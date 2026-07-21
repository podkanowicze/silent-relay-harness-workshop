# Design Notes 05–12 — Grounded Product Pairs

Status: **all eight concepts approved and expanded into full exercises**.

The standard is exercise 01, carpool, and bike service: two familiar products that naturally share the same controls, forms, prices, availability, reservations, and confirmations.

| # | Concept | Status |
|---|---|---|
| 05 | [Visitor Parking Pool](05-visitor-parking-pool.md) | finalised |
| 06 | [Restaurant Floor Planner](06-restaurant-floor-planner.md) | finalised |
| 07 | [Club Kit Pool](07-club-kit-pool.md) | finalised |
| 08 | [Community Fridge Pickup](08-community-fridge-pickup.md) | finalised |
| 09 | [Company Van Load Planner](09-company-van-load-planner.md) | finalised |
| 10 | [Exam Seating Planner](10-exam-seating-planner.md) | finalised |
| 11 | [Apartment Maintenance Board](11-apartment-maintenance-board.md) | finalised |
| 12 | [Book Club Set Request](12-book-club-set-request.md) | finalised |

## 05 — Visitor Parking Pool

- Intended product: an internal company page that allocates limited visitor-parking permits requested by employees.
- Natural drift: a public paid-parking booking page.
- Early sequence: location/date/time search → show spaces → price/cost information → select bay.
- Late context reveal: employee host, visitor purpose, accessible-bay rules, permit approval.
- Pivotal feature: “Reserve a space” either submits an internal permit request or purchases parking.
- Visual final fork: `Permit awaiting host/security approval` versus QR parking ticket and payment receipt.

## 06 — Restaurant Floor Planner

- Intended product: an internal restaurant floor plan used by the host team to seat reservations that already exist and track which tables need resetting.
- Natural drift: a customer-facing table-reservation page.
- Early sequence: choose date/time and party size → show floor map → display table capacity and availability → select a table.
- Later operational data: existing reservation reference, table-cleaning state, accessibility fit, tables that may be combined, and server section.
- Pivotal feature: “Confirm table” either assigns an existing reservation to a ready table or creates a brand-new booking.
- Natural code fork: `existingReservations/tableReadiness/seatingAssignments` versus `booking/selectedTable/guestDetails`.
- Visual final fork: host stand with `Waiting / Seated / Needs reset` versus booking reference, guest confirmation, and cancellation policy.

## 07 — Club Kit Pool

- Intended product: an internal sports-club page that allocates club-owned shirts, shorts, jackets, and equipment to already-registered players for a season or tournament.
- Natural drift: an online sportswear shop.
- Early sequence: product catalogue → size and colour variants → stock count → select items → basket-like summary → replacement value.
- Later allocation data: registered player, team, tournament, mandatory kit set, return date, issued condition, and club ownership.
- Pivotal feature: “Submit order” either requests a temporary kit allocation or purchases clothing.
- Natural code fork: `kitAssets/playerAllocation/returnDue` versus `products/cart/customerOrder`.
- Visual final fork: asset tags and return checklist versus delivery address, payment, and order number.

## 08 — Community Fridge Pickup

- Intended product: free allocation of donated surplus food into timed community pickups.
- Natural drift: grocery e-commerce checkout.
- Early sequence: product cards → quantities → expiry → select items → pickup slot → order summary.
- Late context reveal: no prices, household limits, allergen visibility, fairness rules, unclaimed-food release.
- Pivotal feature: “Submit order” either requests a free pickup allocation or creates a grocery purchase.
- Visual final fork: allocation pending and £0 versus basket total, payment, and purchase confirmation.

## 09 — Company Van Load Planner

- Intended product: an internal warehouse page for assigning company parcels to van runs that are already scheduled.
- Natural drift: a public courier-booking and parcel-tracking page.
- Early sequence: origin/destination/date → parcel size and weight → available vehicle capacity → select service → show cost.
- Later operational data: internal department, existing van run, loading order, fragile/hazard incompatibilities, driver capacity, and depot handoff.
- Pivotal feature: “Book collection” either adds an internal parcel to an existing company route or buys courier service.
- Natural code fork: `scheduledVanRuns/loadItems/departmentCost` versus `shippingServices/parcelOrder/fare`.
- Visual final fork: van load diagram and driver approval versus shipping label, tracking number, and payment receipt.

## 10 — Exam Seating Planner

- Intended product: an internal school or university page that assigns already-registered exam candidates to rooms and seats.
- Natural drift: a cinema or event ticket-booking page.
- Early sequence: choose session → show room and seat map → display available seats → select a seat → add participant details.
- Later allocation data: candidate number, exam version, accessibility arrangement, separation rules, invigilator zones, and room capacity.
- Pivotal feature: “Reserve seat” either creates an internal exam allocation or issues an event ticket.
- Natural code fork: `examCandidates/seatAssignments/examVersion` versus `attendees/reservations/tickets`.
- Visual final fork: invigilator seating list and candidate labels versus QR ticket, booking reference, and purchase confirmation.

## 11 — Apartment Maintenance Board

- Intended product: a shared internal to-do list used by a housing team after a repair report already exists.
- Natural drift: a tenant-facing marketplace for ordering a tradesperson.
- Early sequence: to-do list → calendar → repair category → available times → estimate → scheduling form.
- Late context reveal: existing case number, keys/access status, parts blocker, internal inspection, tenant contact handled elsewhere.
- Pivotal feature: “Confirm visit” either schedules internal work against an existing case or books a paid contractor.
- Visual final fork: case tasks and property access checklist versus service catalogue, checkout, and appointment confirmation.

## 12 — Book Club Set Request

- Intended product: library staff collect group interest before borrowing a multi-copy book-club set from another branch.
- Natural drift: an online bookstore selling individual copies.
- Early sequence: book catalogue → minimum group size → available copies → select title → cost/replacement value → reservation.
- Late context reveal: library-card group, discussion date, inter-branch request, return date, no individual ownership.
- Pivotal feature: “Confirm order” either sends an inter-library set request or purchases books.
- Visual final fork: `Group 7/8 — request pending branch approval` versus quantity, delivery, payment, and order number.

## Recommended order for review

1. Visitor Parking Pool
2. Exam Seating Planner
3. Restaurant Floor Planner
4. Community Fridge Pickup
5. Company Van Load Planner
6. Club Kit Pool
7. Book Club Set Request
8. Apartment Maintenance Board

Visitor Parking and Exam Seating have the clearest visual fork. Restaurant Floor Planner is also strong, but its `existing reservation` boundary must be very visible in `SPEC-0`. Apartment Maintenance remains last because it overlaps with the accepted bike-service exercise.
