from workshop_runner.catalog import load_catalog, select_exercises
from workshop_runner.routing import route_for_all_stages

from .helpers import ROOT


def test_catalog_contains_twelve_complete_exercises():
    catalog = load_catalog(ROOT)
    assert len(catalog) == 12
    assert [item.number for item in sorted(catalog.values(), key=lambda item: item.number)] == list(range(1, 13))
    assert all(sorted(exercise.deltas) == list(range(1, 13)) for exercise in catalog.values())
    assert all(len(exercise.spec0) > 1_000 for exercise in catalog.values())


def test_default_selection_uses_participant_count():
    catalog = load_catalog(ROOT)
    selected = select_exercises(catalog, (), 2)
    assert [exercise.number for exercise in selected] == [1, 2]


def test_twelve_person_route_visits_every_non_author_once():
    route = route_for_all_stages(
        author_slot=1, participant_count=12, routing_mode="skip_author"
    )
    assert route[0] == 1
    assert len(route) == 12
    assert set(route[1:]) == set(range(2, 13))


def test_smaller_workshop_repeats_only_non_authors():
    route = route_for_all_stages(
        author_slot=1, participant_count=4, routing_mode="skip_author"
    )
    assert route[:7] == [1, 2, 3, 4, 2, 3, 4]
    assert 1 not in route[1:]


def test_two_person_manual_route_is_circular():
    route = route_for_all_stages(
        author_slot=1, participant_count=2, routing_mode="circular"
    )
    assert route == [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]


def test_two_person_skip_author_keeps_the_only_non_author():
    route = route_for_all_stages(
        author_slot=1, participant_count=2, routing_mode="skip_author"
    )
    assert route == [1] + [2] * 11

