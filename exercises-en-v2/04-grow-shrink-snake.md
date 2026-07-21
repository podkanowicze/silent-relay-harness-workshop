# 04 — Grow / Shrink Snake

Shared mechanics: [Workshop Rules](../exercises-en/00-workshop-rules.md).

## The actual game twist

This is a real Snake game with two permanent pickup types:

- a growth pickup adds body segments;
- a shrink pickup removes tail segments;
- both pickups become more powerful the longer they remain uncollected;
- a hunger timer forces the player to collect something regularly;
- collecting only growth eventually makes navigation impossible;
- collecting only shrink eventually reaches the minimum length and no longer resets hunger;
- therefore a long run requires fast, deliberate use of both.

The likely drift is not into another application. It is into ordinary Snake where only the growth pickup matters and the shrink/balance loop becomes cosmetic or broken.

## Backward design

| Late feature | Earlier rule it depends on | Generic implementation after context loss |
|---|---|---|
| hunger timer | resets only when a pickup actually changes length | resets on any food or disappears entirely |
| dynamic potency | each pickup ages independently and visibly | fixed `+1/-1` food |
| scoring | rewards fast collection and successful length change | points only for growth food |
| difficulty | increases game speed without changing pickup rules | adds unrelated enemies or walls |
| result screen | explains growth/shrink balance and missed hunger | ordinary apple score and high score |

## `SPEC-0` image

### Grow / Shrink Snake

Build a polished browser Snake game on a visible 24-by-18 grid. The snake starts at length six near the centre and moves right every 140 ms. Arrow keys and WASD control direction. Only one direction change may be queued between ticks, and direct reversal is forbidden. The board has solid boundaries and self-collision ends the run.

Two pickups are always present: a magenta **Growth Orb** and a cyan **Shrink Orb**. Neither may spawn on the snake or the other pickup. After collection or expiry, that pickup respawns independently on a valid cell.

Each pickup has an age and visible potency ring. The orb visibly enlarges inside its cell as potency rises, while its collision cell stays unchanged. From 0–2 seconds its effect is one segment; after 2 seconds it becomes two; after 4 seconds it becomes three. At 6 seconds it expires and respawns at potency one. Collecting a Growth Orb adds its current potency to the body. Collecting a Shrink Orb removes its potency from the tail, but the snake may never become shorter than three cells.

A ten-second hunger timer creates urgency. It resets only when a pickup changes the snake’s length. A Shrink Orb collected at minimum length gives no points and does not reset hunger. If hunger reaches zero, the run ends. This makes both pickups necessary: uncontrolled growth makes the board harder to navigate, while repeated shrinking eventually stops feeding the hunger timer.

Fast collection scores more. A successful pickup gives `40 - 5 × whole seconds of age`, with a minimum of 10 points, multiplied by the number of segments actually added or removed. The HUD shows score, length, hunger, both pickup ages/potencies, run time, speed, and state separately.

Every 30 seconds, the movement tick decreases by 10 ms, never below 80 ms. Pickup age and hunger use real elapsed game time and pause with the game. Space pauses/resumes; `R` restarts every timer and state.

Use a dark neutral background, lime snake, magenta Growth Orb, cyan Shrink Orb, and clear potency rings. Reduced-motion mode removes pulsing but not timers. Touch controls appear on narrow screens. The final result shows score, run time, maximum length, minimum length, growth segments, shrink segments, hunger/collision cause, and local personal best.

## `DELTA-1` — only the original author sees this with `SPEC-0`

```text
Create a 24-by-18 game grid and render a six-cell snake near the centre.
Add a Start control; after starting, move the snake one cell to the right
every 140 ms. Make the head visually distinct. Do not add pickups, score,
collision handling, or other gameplay yet.
```

The author has eight minutes and empty `index.html`, `styles.css`, and `app.js`.

## `DELTA-2…12`

| D | Participant card | Required result | Likely loss of the twist |
|---|---|---|---|
| 2 | **Add keyboard controls using Arrow keys and WASD. Accept at most one queued direction change between movement ticks, prevent direct reversal, and prevent the page from scrolling when game keys are used.** | Reliable grid control with no reversal exploit. | Multiple buffered turns or standard loose input. |
| 3 | **Add a magenta Growth Orb. It must spawn only on an empty cell; collecting it adds one body segment and immediately respawns it on another valid cell.** | First half of the length-management loop. | Treated as the game’s ordinary apple and primary objective. |
| 4 | **Add a cyan Shrink Orb that exists at the same time as the Growth Orb. Collecting it removes one tail segment, never reduces length below three, and respawns it independently.** | Both choices stay visible; shrinking is real gameplay. | Shrink becomes a rare bonus, score penalty, or decorative power-up. |
| 5 | **Make each pickup visibly enlarge and grow in potency while it remains on the board, without changing its one-cell collision area. Its effect is one segment for 0–2 seconds, two after 2 seconds, and three after 4 seconds; show age and potency, then expire and respawn it at 6 seconds.** | Independent timers and visible escalating consequences. | Fixed effects, shared timer, or visual growth without mechanical effect. |
| 6 | **Add a ten-second hunger timer. Reset it only when a collected pickup actually changes snake length; reaching zero ends the run. A Shrink Orb collected at length three must neither score nor reset hunger.** | The player must eventually use both pickup types. | Any pickup resets hunger, allowing shrink-only survival. |
| 7 | **Add scoring and the full HUD. A successful pickup scores `(40 - 5 × whole age seconds) × segments changed`, with a minimum base of 10; show score, length, hunger, both pickup ages, run time, speed, and state separately.** | Fast, effective balancing is rewarded. | Growth gives points; shrinking is punished or ignored. |
| 8 | **Add collision and game-over handling. End the run on boundary collision, self-collision, or hunger expiry; freeze movement and both pickup timers, and show the exact cause. The board must not wrap.** | Three coherent failure modes. | Generic Snake collision only; hunger continues after death. |
| 9 | **Add Pause, Resume, and Restart. Space toggles pause; `R` starts a clean run. Pause must freeze movement, hunger, pickup ageing, and run time; restart resets every timer, pickup, score, length statistic, and direction.** | One consistent game clock. | Visual pause while timers continue; stale pickup effects after restart. |
| 10 | **Add time-based difficulty. Every 30 seconds of active play, reduce the movement tick by 10 ms from its 140 ms start, never below 80 ms. Show the next speed change without altering hunger or pickup timing.** | Difficulty increases while the core loop stays stable. | Pickup effects or hunger speed up too; unrelated obstacles added. |
| 11 | **Complete responsive design and accessibility. Add labelled touch controls on narrow screens, reduced-motion and high-contrast toggles, visible keyboard focus, and distinct shape as well as colour for the two pickups. Gameplay timing must remain identical.** | Twist remains readable without relying only on colour. | Accessibility setting changes speed/potency or makes pickups ambiguous. |
| 12 | **Add a final results screen and local personal best. Show score, run time, maximum and minimum length, segments grown and removed, failure cause, and Play again; restarting must create exactly the original six-cell state.** | Results reveal whether the player balanced both effects. | Ordinary apple score and longest-length leaderboard. |

## The pivotal state after `DELTA-6`

### Twist preserved

```js
const pickups = {
  grow: { ageMs: 1600, potency: 1 },
  shrink: { ageMs: 4300, potency: 3 }
};
const run = { length: 8, hungerMs: 6200, minLength: 3 };
```

The player sees two simultaneous decisions: a safe small growth now or a strong shrink before it expires.

### Twist lost

```js
const food = { type: "grow", points: 10 };
const powerUps = [{ type: "shrink", active: true }];
```

The game has become normal Snake with an occasional shrink bonus. Hunger and results will naturally focus on the growth food.

## What the original author can verify quickly

1. Both pickups exist simultaneously and respawn independently.
2. A pickup visibly changes from potency one to two to three.
3. Growth adds exactly its potency; shrink removes exactly its potency down to length three.
4. A no-effect shrink at length three gives no score and does not reset hunger.
5. A fast pickup scores more than the same pickup collected late.
6. Avoiding all pickups ends the run after ten seconds.
7. Pause freezes movement, hunger, pickup age, and run time.
8. At 30 seconds only movement speed changes.
9. Reduced motion changes no timer.
10. Final results show both grown and removed segments.
