"""Lesson 02 - distance metrics: what role_transition_distance actually computes.

Run:  make learn      (or)      .venv/bin/python learning/02_distance_metrics.py

This one uses the real code and the real example profiles, so the numbers here
are the same numbers `make demo` prints. Three ways to measure how far apart two
role vectors are, and a genuine design decision about which one is correct.
"""

from __future__ import annotations

from math import sqrt
from pathlib import Path

from carryover_football.roles import DIMENSIONS, compare_roles, load_role_profile

EXAMPLES = Path(__file__).resolve().parents[1] / "examples" / "data"


def rule(title: str) -> None:
    print(f"\n{title}\n{'-' * len(title)}")


def l1_distance(a: list[float], b: list[float]) -> float:
    """Mean absolute gap. Every dimension counts the same."""
    return sum(abs(x - y) for x, y in zip(a, b, strict=True)) / len(a)


def l2_distance(a: list[float], b: list[float]) -> float:
    """Euclidean. Squaring means big gaps dominate small ones."""
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b, strict=True)))


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Angle between the vectors. Compares SHAPE and ignores magnitude."""
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    norm_a = sqrt(sum(x * x for x in a))
    norm_b = sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b)


def part_one_the_vectors(origin: list[float], destination: list[float]) -> None:
    rule("1. The two role vectors")
    print("Origin is what the player DID. Destination is what the new team ASKS.")
    print()
    print(f"  {'dimension':<18} {'origin':>7} {'dest':>7} {'delta':>8} {'|delta|':>8}")
    for name, o, d in zip(DIMENSIONS, origin, destination, strict=True):
        print(f"  {name:<18} {o:>7.2f} {d:>7.2f} {d - o:>+8.2f} {abs(d - o):>8.2f}")
    total = sum(abs(d - o) for o, d in zip(origin, destination, strict=True))
    print(f"  {'':<18} {'':>7} {'':>7} {'sum':>8} {total:>8.2f}")


def part_two_three_metrics(origin: list[float], destination: list[float]) -> None:
    rule("2. Three ways to say 'how far apart are these?'")

    l1 = l1_distance(origin, destination)
    l2 = l2_distance(origin, destination)
    cos = cosine_similarity(origin, destination)

    total = sum(abs(d - o) for o, d in zip(origin, destination, strict=True))
    print(f"  L1 (mean absolute gap)  {total:.2f} / {len(DIMENSIONS)} = {l1:.4f}")
    print(f"  L2 (Euclidean)                       = {l2:.4f}")
    print(f"  cosine similarity                    = {cos:.4f}")
    print()
    print("Read those three numbers and notice they tell different stories.")
    print()
    print(f"  cosine {cos:.3f} says: 'these are almost the same shape'")
    print(f"  L1     {l1:.3f} says: 'the average dimension moved by 0.15'")


def part_three_why_not_cosine(origin: list[float], destination: list[float]) -> None:
    rule("3. Why cosine would be the WRONG choice here")

    norm_o = sqrt(sum(x * x for x in origin))
    norm_d = sqrt(sum(x * x for x in destination))
    print(f"  length of origin vector      = {norm_o:.4f}")
    print(f"  length of destination vector = {norm_d:.4f}")
    print()
    print("The destination vector is LONGER. The new team wants more of nearly")
    print("everything: more pressing, more link play, more depth running.")
    print()
    print("Cosine only measures the angle between the vectors, so it treats")
    print("'the same shape, scaled up' as no difference at all. That is exactly")
    print("the wrong behaviour for role demand, because 'more of everything' is")
    print("a real and demanding change for a player, not a rescaling artifact.")
    print()
    print("Cosine is the right tool when you want 'who plays like this player,")
    print("regardless of volume'. It is the wrong tool for 'how much more will")
    print("be asked of him'. Same maths, different question.")


def part_four_l1_versus_l2(origin: list[float], destination: list[float]) -> None:
    rule("4. L1 or L2? A real design decision")

    gaps = sorted(
        (
            (abs(d - o), n)
            for n, o, d in zip(DIMENSIONS, origin, destination, strict=True)
        ),
        reverse=True,
    )
    print("  gaps, largest first:")
    for gap, name in gaps:
        print(f"    {name:<18} {gap:.2f}   squared: {gap**2:.4f}")
    print()
    print("Squaring is what separates L2 from L1. The two biggest gaps here")
    print(f"({gaps[0][1]} and {gaps[1][1]}) contribute most of L2, while in L1")
    print("every dimension carries equal weight.")
    print()
    print("So:")
    print("  L2 answers 'how bad is the WORST mismatch?'")
    print("  L1 answers 'how much change on an AVERAGE dimension?'")
    print()
    print("Carryover uses L1 for the headline number and lists the largest gaps")
    print("separately. That is a deliberate split: one number that is honestly")
    print("an average, plus the specific dimensions a coach should look at. If")
    print("L2 were the headline, one extreme dimension could dominate a summary")
    print("that reads like it describes the whole profile.")


def part_five_the_code_agrees(origin_path: Path, destination_path: Path) -> None:
    rule("5. The package computes the same thing")
    transition = compare_roles(
        load_role_profile(origin_path), load_role_profile(destination_path)
    )
    print(
        f"  compare_roles(...).role_transition_distance = "
        f"{transition.role_transition_distance:.4f}"
    )
    print()
    print("Which is the number `make demo` prints, and the number the CLI test")
    print("asserts. You have been computing a normalised L1 distance all along.")


def main() -> None:
    origin_path = EXAMPLES / "synthetic_origin_role.json"
    destination_path = EXAMPLES / "synthetic_destination_role.json"
    origin_profile = load_role_profile(origin_path)
    destination_profile = load_role_profile(destination_path)

    origin = [origin_profile.value_for(d) for d in DIMENSIONS]
    destination = [destination_profile.value_for(d) for d in DIMENSIONS]

    print("=" * 72)
    print("LESSON 02 - DISTANCE METRICS")
    print("=" * 72)
    part_one_the_vectors(origin, destination)
    part_two_three_metrics(origin, destination)
    part_three_why_not_cosine(origin, destination)
    part_four_l1_versus_l2(origin, destination)
    part_five_the_code_agrees(origin_path, destination_path)

    rule("Check it yourself")
    print("  |deltas| = 0.12, 0.07, 0.24, 0.09, 0.25, 0.12")
    print("  sum      = 0.89")
    print("  L1 mean  = 0.89 / 6 = 0.1483")
    print()
    print("Takeaway: the metric you pick encodes the question you are asking.")


if __name__ == "__main__":
    main()
