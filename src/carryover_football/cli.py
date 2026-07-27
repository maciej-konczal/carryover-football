"""Command-line interface for role-transition comparisons."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from carryover_football.roles import (
    DimensionComparison,
    RoleProfileError,
    compare_roles,
    load_role_profile,
)

DISCLAIMER = (
    "THIS IS NOT A PROBABILITY, RISK PERCENTAGE, OR PREDICTION.\n"
    "The role-transition distance is a descriptive index only."
)


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Compare a striker's origin behavior with destination role demand."
        )
    )
    parser.add_argument("origin", help="path to the origin role JSON profile")
    parser.add_argument("destination", help="path to the destination role JSON profile")
    return parser


def _format_ranked(
    heading: str, comparisons: tuple[DimensionComparison, ...]
) -> list[str]:
    lines = [heading]
    if not comparisons:
        lines.append("  None")
    else:
        lines.extend(f"  {item.dimension}: {item.delta:+.2f}" for item in comparisons)
    return lines


def format_report(origin_path: str, destination_path: str) -> str:
    """Create a human-readable role-transition report."""
    origin = load_role_profile(origin_path)
    destination = load_role_profile(destination_path)
    transition = compare_roles(origin, destination)

    lines = [
        "CARRYOVER — ROLE-TRANSITION COMPARISON",
        f"Origin profile: {origin_path}",
        f"Destination profile: {destination_path}",
        "",
        "Per-dimension comparison",
        "dimension             origin  destination   delta  absolute gap",
    ]
    lines.extend(
        f"{item.dimension:<21} "
        f"{item.origin_behavior:>6.2f} "
        f"{item.destination_demand:>12.2f} "
        f"{item.delta:>+7.2f} "
        f"{item.absolute_gap:>13.2f}"
        for item in transition.dimensions
    )
    lines.extend([""])
    lines.extend(
        _format_ranked("Two largest new demands:", transition.largest_new_demands())
    )
    lines.extend([""])
    lines.extend(
        _format_ranked(
            "Two most de-emphasized behaviors:", transition.most_deemphasized()
        )
    )
    lines.extend(
        [
            "",
            (
                "Overall role-transition distance: "
                f"{transition.role_transition_distance:.3f}"
            ),
            "",
            "=" * 62,
            DISCLAIMER,
            "=" * 62,
        ]
    )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the Carryover role-transition command."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        report = format_report(args.origin, args.destination)
    except (OSError, RoleProfileError) as error:
        parser.error(str(error))

    print(report)
    return 0
