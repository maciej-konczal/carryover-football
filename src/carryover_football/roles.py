"""Role-profile validation and transparent transition calculations."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from statistics import fmean
from typing import Any

DIMENSIONS = (
    "depth_running",
    "box_presence",
    "link_play",
    "aerial_play",
    "pressing",
    "chance_creation",
)


class RoleProfileError(ValueError):
    """Raised when a role profile does not match the required schema."""


@dataclass(frozen=True)
class RoleProfile:
    """A striker role represented by the six fixed behavior dimensions."""

    depth_running: float
    box_presence: float
    link_play: float
    aerial_play: float
    pressing: float
    chance_creation: float

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> RoleProfile:
        """Validate and construct a role profile from a mapping."""
        if not isinstance(data, Mapping):
            raise RoleProfileError("role profile must be a JSON object")

        keys = set(data)
        expected = set(DIMENSIONS)
        missing = expected - keys
        extra = keys - expected

        if missing:
            raise RoleProfileError(
                f"missing role dimensions: {', '.join(sorted(missing))}"
            )
        if extra:
            raise RoleProfileError(
                f"unexpected role dimensions: {', '.join(sorted(extra))}"
            )

        values: dict[str, float] = {}
        for dimension in DIMENSIONS:
            value = data[dimension]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise RoleProfileError(
                    f"{dimension} must be a number between 0.0 and 1.0"
                )
            numeric_value = float(value)
            if not 0.0 <= numeric_value <= 1.0:
                raise RoleProfileError(f"{dimension} must be between 0.0 and 1.0")
            values[dimension] = numeric_value

        return cls(**values)

    def value_for(self, dimension: str) -> float:
        """Return the value for one of the fixed role dimensions."""
        if dimension not in DIMENSIONS:
            raise KeyError(f"unknown role dimension: {dimension}")
        return getattr(self, dimension)


@dataclass(frozen=True)
class DimensionComparison:
    """The transparent difference for one role dimension."""

    dimension: str
    origin_behavior: float
    destination_demand: float

    @property
    def delta(self) -> float:
        """Destination demand minus origin behavior."""
        return self.destination_demand - self.origin_behavior

    @property
    def absolute_gap(self) -> float:
        """The unsigned size of the role change."""
        return abs(self.delta)


@dataclass(frozen=True)
class RoleTransition:
    """A descriptive comparison between origin and destination roles."""

    dimensions: tuple[DimensionComparison, ...]

    @property
    def role_transition_distance(self) -> float:
        """Mean absolute gap across all six dimensions."""
        return fmean(item.absolute_gap for item in self.dimensions)

    def largest_new_demands(self, limit: int = 2) -> tuple[DimensionComparison, ...]:
        """Return up to ``limit`` dimensions with the largest positive deltas."""
        positive = (item for item in self.dimensions if item.delta > 0.0)
        return tuple(sorted(positive, key=lambda item: -item.delta)[:limit])

    def most_deemphasized(self, limit: int = 2) -> tuple[DimensionComparison, ...]:
        """Return up to ``limit`` dimensions with the most negative deltas."""
        negative = (item for item in self.dimensions if item.delta < 0.0)
        return tuple(sorted(negative, key=lambda item: item.delta)[:limit])


def compare_roles(origin: RoleProfile, destination: RoleProfile) -> RoleTransition:
    """Compare origin behavior with destination demand in fixed dimension order."""
    return RoleTransition(
        dimensions=tuple(
            DimensionComparison(
                dimension=dimension,
                origin_behavior=origin.value_for(dimension),
                destination_demand=destination.value_for(dimension),
            )
            for dimension in DIMENSIONS
        )
    )


def load_role_profile(path: str | Path) -> RoleProfile:
    """Load and validate a role profile from a JSON file."""
    profile_path = Path(path)
    try:
        with profile_path.open(encoding="utf-8") as profile_file:
            data = json.load(profile_file)
    except json.JSONDecodeError as error:
        message = f"invalid JSON in {profile_path}: {error.msg}"
        raise RoleProfileError(message) from error

    return RoleProfile.from_mapping(data)
