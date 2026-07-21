# Shared Workshop Rules

## Purpose

Show that an agent inherits files, not product intent. After 12 locally reasonable changes, an application may still work while serving a different user, making a different decision, or crossing a boundary the original author considered essential.

## UI and harness

- Participants use Deep Agents Code through a workshop UI.
- Each application has a folder containing three empty, existing files: `index.html`, `styles.css`, `app.js`.
- The harness may edit only those files and blocks all new files and directories.
- At the start of every turn, the UI creates a completely fresh conversation and points Deep Agents Code at the current application folder.
- A read-only panel beside the chat shows the previous agent’s final message.
- That message is not injected into the new conversation. The participant decides what to carry into their prompt.
- The UI shows the agent’s terminal-like activity live.
- The page preview refreshes after edits.

## Timing

| Time | Activity |
|---|---|
| 0–10 min | context engineering introduction |
| 10–15 min | UI and routing demonstration |
| 15–23 min | round 1: eight-minute bootstrap from empty files |
| 23–67 min | rounds 2–12: eleven four-minute changes |
| 67–71 min | final implementers describe the products |
| 71–81 min | original authors review their returned applications |
| 81–88 min | compare drift points |
| 88–90 min | conclusions |

The timer does not restart after another prompt. Prompt count and final-message length are not limited.

## Round 1

The original author sees only:

- the three empty files;
- an image containing `SPEC-0`;
- `DELTA-1`;
- the shared technical rules.

The image is outside the folder and agent context. It cannot be attached to the agent or processed with OCR. The author may communicate any selected context in their own words.

The author builds the smallest working page needed for `DELTA-1`. `SPEC-0` is the product constitution, not an instruction to pre-implement future features. The author does not see `DELTA-2…12`.

## Rounds 2–12

The next participant sees only:

- the current three files and live preview;
- the previous agent’s last message in the side panel;
- the current delta card;
- a fresh chat.

They do not see `SPEC-0`, previous prompts, reasoning, conversations, or other delta cards.

## Routing

With 12 people, an application is changed once by its author and then once by each of the other 11 people.

With fewer than 12 people, the application keeps circulating among non-authors. After every eligible person has handled it, another lap begins. Its original author is skipped throughout `DELTA-2…12`, and nobody should receive the same application twice in succession.

## Final interpretation and author review

After implementing `DELTA-12`, the last non-author answers without agent assistance:

```text
1. This application is for:
2. Its primary user is:
3. Its final action causes:
```

Only then does the application return to its original author. The author receives the final app, the original `SPEC-0`, all 12 delta cards, the last agent message, and the final implementer’s interpretation. The author reviews but does not repair the app.

## Context-transfer rules

- No `.md`, `.txt`, handoff, documentation, or other new files.
- Do not hide the full specification in comments, string constants, invisible DOM, or encoded data.
- Visible UI language, appropriate data structures, meaningful names, and ordinary technical comments are valid context carriers.
- A context-rich final message written in the participant’s own words is a successful strategy.
- The harness flags `copy-through` if a final answer contains 20 consecutive normalized words from `SPEC-0`, or three distinct 12-word sequences. Flagged chains remain useful for discussion but are excluded from drift-rate measurement.

## Product constraints

- Vanilla HTML, CSS, and JavaScript only.
- No framework, build step, backend, network, dependency installation, or external side effect.
- Every delta must make a visible, usable change.
- Correct and drifted versions must both be coherent applications.
- Humor may appear in the story, sample data, or microcopy, while the interface remains professionally plausible.
- Hidden checks observe behavior and visible meaning; they do not repair drift during the chain.
