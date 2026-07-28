"""Lesson 03 - percentiles, z-scores, and the question nobody asks.

Run:  make learn      (or)      .venv/bin/python learning/03_percentiles_and_zscores.py

A raw number like "0.52 npxG per 90" means nothing on its own. To make it mean
something you compare it to other players, and there are two standard ways to do
that. They disagree, and the disagreement matters.

Then the harder question, which is the real content of this lesson: compared to
WHICH other players? That choice is usually made silently and it moves the
answer more than the choice of method does.
"""

from __future__ import annotations

from statistics import mean, pstdev

# Eleven strikers' non-penalty expected goals per 90, sorted. Small enough that
# every number below can be checked with a calculator.
POPULATION = [0.28, 0.31, 0.35, 0.38, 0.42, 0.45, 0.49, 0.52, 0.58, 0.64, 0.95]

# The player we will follow through the lesson.
PLAYER = 0.52


def rule(title: str) -> None:
    print(f"\n{title}\n{'-' * len(title)}")


def percentile_of(value: float, population: list[float]) -> float:
    """Rank position, scaled to 0-100.

    The lowest value in the population scores 0 and the highest scores 100.
    Only the ORDER matters: how far apart the values are is discarded.
    """
    ordered = sorted(population)
    rank = ordered.index(value)
    return 100.0 * rank / (len(ordered) - 1)


def z_score_of(value: float, population: list[float]) -> float:
    """How many standard deviations from the mean.

    Unlike a percentile this keeps the DISTANCES, so an extreme value stays
    visibly extreme instead of being flattened to "top of the list".
    """
    return (value - mean(population)) / pstdev(population)


def part_one_raw_numbers_mean_nothing() -> None:
    rule("1. A number with no context")
    print(f"A striker records {PLAYER} npxG per 90.")
    print()
    print("Good? Bad? Unanswerable. You need a comparison group, and the")
    print("moment you pick one you have made a modelling decision.")
    print()
    print("Our comparison group, 11 strikers:")
    print(f"  {POPULATION}")
    print(f"  mean = {mean(POPULATION):.4f}")
    print(f"  sd   = {pstdev(POPULATION):.4f}")


def part_two_two_methods() -> None:
    rule("2. Two ways to place a player in that group")
    print("  value   percentile   z-score")
    for value in POPULATION:
        marker = "   <-- our player" if value == PLAYER else ""
        print(
            f"  {value:>5.2f}   {percentile_of(value, POPULATION):>9.0f}   "
            f"{z_score_of(value, POPULATION):>+7.2f}{marker}"
        )
    print()
    print("Both orderings are identical, as they must be. Look at the SPACING.")


def part_three_where_they_disagree() -> None:
    rule("3. Where the two methods disagree")
    best, second = 0.95, 0.64
    print(
        f"  {second}: percentile {percentile_of(second, POPULATION):.0f}, "
        f"z-score {z_score_of(second, POPULATION):+.2f}"
    )
    print(
        f"  {best}: percentile {percentile_of(best, POPULATION):.0f}, "
        f"z-score {z_score_of(best, POPULATION):+.2f}"
    )
    print()
    gap_pct = percentile_of(best, POPULATION) - percentile_of(second, POPULATION)
    gap_z = z_score_of(best, POPULATION) - z_score_of(second, POPULATION)
    print(f"  percentile gap: {gap_pct:.0f} points")
    print(f"  z-score gap:    {gap_z:.2f} standard deviations")
    print()
    print("Percentile says these two are neighbours. The z-score says one of")
    print("them is in a different category of player. Both are true statements")
    print("about the same pair of numbers.")

    rule("4. But the z-score has its own problem")
    deviations = [(v - mean(POPULATION)) ** 2 for v in POPULATION]
    top_share = max(deviations) / sum(deviations)
    print("The standard deviation is built from squared distances to the mean,")
    print("so the outlier dominates it:")
    print()
    print(f"  total squared deviation      = {sum(deviations):.4f}")
    print(f"  contributed by {max(POPULATION)} alone   = {max(deviations):.4f}")
    print(f"  that is {top_share:.0%} of the entire spread, from ONE player.")
    print()
    print("Remove him and every other z-score in the table changes. Percentiles")
    print("would barely move. That is the trade:")
    print()
    print("  percentile: robust to outliers, throws away magnitude")
    print("  z-score:    keeps magnitude, distorted by outliers")
    print()
    print("Neither is correct in general. Pick the one that matches the claim")
    print("you want to make, and say which you used.")


def part_five_against_whom() -> None:
    rule("5. The question that matters more than either method")

    europe = POPULATION
    elite = [0.49, 0.52, 0.58, 0.64, 0.95]
    weaker = [0.28, 0.31, 0.35, 0.38, 0.42, 0.45, 0.52]

    print(f"The SAME player, the same {PLAYER} npxG per 90, three comparison")
    print("groups:\n")
    groups = [
        ("all 11 strikers", europe),
        ("only the elite 5", elite),
        ("only a weaker league", weaker),
    ]
    print("  reference population       n    percentile   z-score")
    for label, group in groups:
        print(
            f"  {label:<24} {len(group):>3}   {percentile_of(PLAYER, group):>9.0f}   "
            f"{z_score_of(PLAYER, group):>+7.2f}"
        )
    print()
    print("Nothing about the player changed. He is simultaneously an elite")
    print("striker, a good one, and a below-average one, depending entirely on")
    print("a choice that is usually made once and never mentioned again.")
    print()
    print("This is why PRD section 22 keeps 'reference population' as an open")
    print("question rather than letting it be decided inside implementation")
    print("code. It is not a detail. It is most of the answer.")


def part_six_back_to_carryover() -> None:
    rule("6. What this means for Carryover")
    print("RoleProfile constrains every dimension to 0.0-1.0. That range is")
    print("percentile-shaped: it implies 'where does this player sit among")
    print("some population', not 'how many actions per 90'.")
    print()
    print("Right now the example profiles are synthetic, so the question is")
    print("hidden. The moment real event data arrives, somebody has to answer:")
    print()
    print("  - all strikers in the big-5, or only this league?")
    print("  - this season only, or a multi-season pool?")
    print("  - all minutes, or only starts?")
    print("  - the same population for the player AND the destination demand?")
    print()
    print("That last one is the subtle one. If a player's behaviour is")
    print("percentiled against Europe but the destination's demand is")
    print("percentiled against Serie A, the delta between them is partly an")
    print("artifact of two different yardsticks, not a real role change.")
    print()
    print("And from lesson 01: a percentile inherits all the noise of whatever")
    print("it ranks. A finishing percentile on 25 shots is a noisy number given")
    print("a precise-looking label, which is the most dangerous kind.")


def main() -> None:
    print("=" * 72)
    print("LESSON 03 - PERCENTILES AND Z-SCORES")
    print("=" * 72)
    part_one_raw_numbers_mean_nothing()
    part_two_two_methods()
    part_three_where_they_disagree()
    part_five_against_whom()
    part_six_back_to_carryover()

    rule("Check it yourself")
    print("  mean = 5.37 / 11                       = 0.4882")
    print("  0.52 is 8th smallest of 11, so rank 7")
    print("  percentile = 100 * 7 / 10              = 70")
    print("  z          = (0.52 - 0.4882) / 0.1803  = +0.18")
    print()
    print("Next: 04, regression to the mean.")


if __name__ == "__main__":
    main()
