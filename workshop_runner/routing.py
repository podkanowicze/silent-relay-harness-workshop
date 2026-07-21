from __future__ import annotations


def next_slot(
    *,
    current_slot: int,
    author_slot: int,
    participant_count: int,
    routing_mode: str,
) -> int:
    """Return the next clockwise participant, optionally skipping the author."""
    if participant_count < 1:
        raise ValueError("participant_count must be positive")
    if routing_mode not in {"circular", "skip_author"}:
        raise ValueError("Unknown routing mode")

    for offset in range(1, participant_count + 1):
        candidate = ((current_slot - 1 + offset) % participant_count) + 1
        if candidate == current_slot:
            continue
        if routing_mode == "skip_author" and candidate == author_slot:
            continue
        return candidate

    # With exactly two people in workshop mode there is only one non-author.
    # That participant must receive consecutive stages, as the author remains skipped.
    if routing_mode == "skip_author" and current_slot != author_slot:
        return current_slot
    if routing_mode == "circular" and participant_count == 1:
        return current_slot
    raise ValueError("No eligible next participant for this routing configuration")


def route_for_all_stages(
    *, author_slot: int, participant_count: int, routing_mode: str
) -> list[int]:
    slots = [author_slot]
    current = author_slot
    for _stage in range(2, 13):
        current = next_slot(
            current_slot=current,
            author_slot=author_slot,
            participant_count=participant_count,
            routing_mode=routing_mode,
        )
        slots.append(current)
    return slots
