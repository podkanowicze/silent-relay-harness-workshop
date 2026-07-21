from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Exercise:
    number: int
    slug: str
    title: str
    spec0: str
    deltas: dict[int, str]
    source_path: Path


class CatalogError(RuntimeError):
    pass


def _document_paths(root: Path) -> list[Path]:
    paths = [root / "exercises-en" / "01-small-town-wings.md"]
    paths.extend(sorted((root / "exercises-en-v2").glob("[0-1][0-9]-*.md")))
    return [path for path in paths if path.name != "05-12-concept-shortlist.md"]


def _extract_code_block(text: str) -> str | None:
    match = re.search(r"```(?:text)?\s*\n(.*?)\n```", text, re.DOTALL)
    return match.group(1).strip() if match else None


def parse_exercise(path: Path) -> Exercise:
    markdown = path.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(\d{2})\s+[—-]\s+(.+?)\s*$", markdown, re.MULTILINE)
    if not title_match:
        raise CatalogError(f"Missing exercise title in {path}")

    number = int(title_match.group(1))
    title = title_match.group(2).strip()
    slug = path.stem

    spec_match = re.search(
        r"^##\s+`SPEC-0` image\s*$\n(?P<body>.*?)^##\s+`DELTA-1`[^\n]*$",
        markdown,
        re.MULTILINE | re.DOTALL,
    )
    if not spec_match:
        raise CatalogError(f"Missing SPEC-0 in {path}")
    spec0 = spec_match.group("body").strip()

    delta1_match = re.search(
        r"^##\s+`DELTA-1`[^\n]*$\n(?P<body>.*?)^##\s+`DELTA-2…12`\s*$",
        markdown,
        re.MULTILINE | re.DOTALL,
    )
    if not delta1_match:
        raise CatalogError(f"Missing DELTA-1 in {path}")
    delta1_body = delta1_match.group("body").strip()
    delta1 = _extract_code_block(delta1_body)
    if not delta1:
        delta1 = re.sub(r"\*\*|`", "", delta1_body).strip()

    deltas: dict[int, str] = {1: delta1}
    row_pattern = re.compile(
        r"^\|\s*(\d{1,2})\s*\|\s*\*\*(.+?)\*\*\s*\|",
        re.MULTILINE,
    )
    for match in row_pattern.finditer(markdown):
        delta_number = int(match.group(1))
        if 2 <= delta_number <= 12:
            deltas[delta_number] = match.group(2).strip()

    if sorted(deltas) != list(range(1, 13)):
        raise CatalogError(
            f"Expected DELTA-1…12 in {path}, found {sorted(deltas)}"
        )
    return Exercise(number, slug, title, spec0, deltas, path)


def load_catalog(root: Path) -> dict[str, Exercise]:
    exercises = [parse_exercise(path) for path in _document_paths(root)]
    by_slug = {exercise.slug: exercise for exercise in exercises}
    if len(exercises) != 12 or len(by_slug) != 12:
        raise CatalogError(f"Expected 12 unique exercises, found {len(by_slug)}")
    return by_slug


def select_exercises(
    catalog: dict[str, Exercise], slugs: tuple[str, ...], participant_count: int
) -> list[Exercise]:
    if slugs:
        missing = [slug for slug in slugs if slug not in catalog]
        if missing:
            raise CatalogError(f"Unknown exercise slug(s): {', '.join(missing)}")
        return [catalog[slug] for slug in slugs]
    return sorted(catalog.values(), key=lambda item: item.number)[:participant_count]
