import json

import pytest

from carryover_football.roles import (
    DIMENSIONS,
    RoleProfile,
    RoleProfileError,
    compare_roles,
    load_role_profile,
)


def profile(**overrides: float) -> RoleProfile:
    values = dict.fromkeys(DIMENSIONS, 0.5)
    values.update(overrides)
    return RoleProfile.from_mapping(values)


def test_compare_roles_calculates_deltas_gaps_and_mean_distance() -> None:
    origin = RoleProfile.from_mapping(
        {
            "depth_running": 0.6,
            "box_presence": 0.8,
            "link_play": 0.4,
            "aerial_play": 0.3,
            "pressing": 0.5,
            "chance_creation": 0.2,
        }
    )
    destination = RoleProfile.from_mapping(
        {
            "depth_running": 0.8,
            "box_presence": 0.7,
            "link_play": 0.6,
            "aerial_play": 0.3,
            "pressing": 0.4,
            "chance_creation": 0.5,
        }
    )

    transition = compare_roles(origin, destination)

    assert [item.delta for item in transition.dimensions] == pytest.approx(
        [0.2, -0.1, 0.2, 0.0, -0.1, 0.3]
    )
    assert [item.absolute_gap for item in transition.dimensions] == pytest.approx(
        [0.2, 0.1, 0.2, 0.0, 0.1, 0.3]
    )
    assert transition.role_transition_distance == pytest.approx(0.15)


def test_rankings_include_only_positive_or_negative_changes() -> None:
    transition = compare_roles(
        profile(),
        profile(
            depth_running=0.7,
            box_presence=0.4,
            link_play=0.8,
            aerial_play=0.3,
        ),
    )

    assert [item.dimension for item in transition.largest_new_demands()] == [
        "link_play",
        "depth_running",
    ]
    assert [item.dimension for item in transition.most_deemphasized()] == [
        "aerial_play",
        "box_presence",
    ]


def test_rankings_use_fixed_dimension_order_to_break_ties() -> None:
    transition = compare_roles(
        profile(),
        profile(depth_running=0.7, box_presence=0.3, link_play=0.7, pressing=0.3),
    )

    assert [item.dimension for item in transition.largest_new_demands()] == [
        "depth_running",
        "link_play",
    ]
    assert [item.dimension for item in transition.most_deemphasized()] == [
        "box_presence",
        "pressing",
    ]


def test_rankings_can_return_fewer_than_two_items() -> None:
    transition = compare_roles(profile(), profile(pressing=0.6))

    assert [item.dimension for item in transition.largest_new_demands()] == ["pressing"]
    assert transition.most_deemphasized() == ()


def test_load_role_profile_from_json(tmp_path) -> None:
    path = tmp_path / "role.json"
    path.write_text(
        json.dumps(dict.fromkeys(DIMENSIONS, 0.5)),
        encoding="utf-8",
    )

    loaded = load_role_profile(path)

    assert loaded.depth_running == 0.5
    assert loaded.chance_creation == 0.5


@pytest.mark.parametrize("invalid_value", [-0.01, 1.01])
def test_rejects_values_outside_unit_interval(invalid_value: float) -> None:
    values = dict.fromkeys(DIMENSIONS, 0.5)
    values["pressing"] = invalid_value

    with pytest.raises(RoleProfileError, match="pressing must be between"):
        RoleProfile.from_mapping(values)


@pytest.mark.parametrize("invalid_value", ["0.5", None, True])
def test_rejects_non_numeric_values(invalid_value) -> None:
    values = dict.fromkeys(DIMENSIONS, 0.5)
    values["link_play"] = invalid_value

    with pytest.raises(RoleProfileError, match="link_play must be a number"):
        RoleProfile.from_mapping(values)


def test_rejects_missing_dimensions() -> None:
    values = dict.fromkeys(DIMENSIONS, 0.5)
    del values["aerial_play"]

    with pytest.raises(RoleProfileError, match="missing.*aerial_play"):
        RoleProfile.from_mapping(values)


def test_rejects_unexpected_dimensions() -> None:
    values = dict.fromkeys(DIMENSIONS, 0.5)
    values["finishing"] = 0.5

    with pytest.raises(RoleProfileError, match="unexpected.*finishing"):
        RoleProfile.from_mapping(values)


def test_rejects_invalid_json(tmp_path) -> None:
    path = tmp_path / "role.json"
    path.write_text("{", encoding="utf-8")

    with pytest.raises(RoleProfileError, match="invalid JSON"):
        load_role_profile(path)
