"""Lesson 01 - sampling variance: why one season of goals proves almost nothing.

Run:  make learn      (or)      .venv/bin/python learning/01_sampling_variance.py

The whole lesson rests on one formula you can check by hand. If a player takes
`n` shots and each shot has an independent chance `p` of going in, the
probability of scoring exactly `k` is the binomial:

    P(k) = C(n, k) * p**k * (1 - p)**(n - k)

Standard library only, so every line is readable.
"""

from __future__ import annotations

from math import comb, sqrt

# A realistic striker season. Deliberately not attached to a named player:
# see the note in learning/README.md about holdout discipline.
SHOTS = 25
EXPECTED_GOALS = 3.6
ACTUAL_GOALS = 1

# Expected goals divided by shots gives the average quality of the chances he
# got. This is the `p` in the formula above.
CHANCE_QUALITY = EXPECTED_GOALS / SHOTS


def binomial(n: int, k: int, p: float) -> float:
    """Probability of exactly k successes in n independent trials."""
    return comb(n, k) * p**k * (1 - p) ** (n - k)


def standard_error(p: float, n: int) -> float:
    """How much an observed rate wobbles around the true rate, by luck alone."""
    return sqrt(p * (1 - p) / n)


def rule(title: str) -> None:
    print(f"\n{title}\n{'-' * len(title)}")


def part_one_the_setup() -> None:
    rule("1. The setup")
    print(f"A striker takes {SHOTS} shots in a season.")
    print(f"Those chances were worth {EXPECTED_GOALS} expected goals in total.")
    print(f"He scores {ACTUAL_GOALS}.")
    print()
    print("The newspapers write that he cannot finish. Can we tell?")
    print()
    print(f"  chance quality p = {EXPECTED_GOALS} / {SHOTS} = {CHANCE_QUALITY:.3f}")
    print(f"  so an average finisher would score about {SHOTS * CHANCE_QUALITY:.1f}")


def part_two_the_distribution() -> None:
    rule("2. What an AVERAGE finisher would have done with those same chances")
    print(
        "Assume he is exactly average: every shot converts at p = "
        f"{CHANCE_QUALITY:.3f}."
    )
    print("Here is how often each goal total comes up, by luck alone:\n")

    print("  goals  probability  ")
    for goals in range(10):
        probability = binomial(SHOTS, goals, CHANCE_QUALITY)
        bar = "#" * round(probability * 100)
        marker = "  <-- what actually happened" if goals == ACTUAL_GOALS else ""
        print(f"  {goals:>5}  {probability:>10.3f}  {bar}{marker}")

    at_most = sum(
        binomial(SHOTS, goals, CHANCE_QUALITY) for goals in range(ACTUAL_GOALS + 1)
    )
    rule("3. The number that matters")
    print(f"P(scoring {ACTUAL_GOALS} or fewer) = ", end="")
    terms = " + ".join(
        f"{binomial(SHOTS, g, CHANCE_QUALITY):.4f}" for g in range(ACTUAL_GOALS + 1)
    )
    print(f"{terms} = {at_most:.4f}")
    print()
    print(
        f"So a perfectly average finisher has this season roughly "
        f"{at_most * 100:.0f}% of the time."
    )
    print(f"That is about 1 season in {1 / at_most:.0f}.")
    print()
    print("In a league with 20 regular strikers, you should EXPECT around")
    print(f"{20 * at_most:.1f} of them to have a 'disaster' season every year,")
    print("with no loss of ability whatsoever. Someone has to be unlucky.")
    print()
    print("This is the whole lesson: a bad goal return is weak evidence.")
    print("It is not zero evidence. It is just much weaker than it feels.")


def part_three_how_many_shots() -> None:
    rule("4. How many shots before finishing skill is measurable?")
    print("The standard error tells us how far an observed rate strays from the")
    print("true rate by chance:  SE = sqrt(p * (1 - p) / n)")
    print()
    print("A rough 95% range is the observed rate plus or minus 2 x SE.\n")
    print("  shots   SE      95% range on conversion    seasons")
    for shots in (25, 50, 100, 200, 400, 800):
        se = standard_error(CHANCE_QUALITY, shots)
        low = max(0.0, CHANCE_QUALITY - 2 * se)
        high = CHANCE_QUALITY + 2 * se
        seasons = shots / SHOTS
        print(
            f"  {shots:>5}   {se:.4f}  {low:>6.1%} to {high:<6.1%}       "
            f"{seasons:>4.0f}"
        )
    print()
    print("At 25 shots the range spans most of the plausible values a striker")
    print("can have. You would need several hundred shots, meaning several")
    print("seasons, before the number pins anything down.")


def part_four_why_behaviour_is_different() -> None:
    rule("5. Why Carryover measures BEHAVIOUR instead")
    print("Compare two things you might measure about the same player.\n")

    # Goals: few trials, low rate. Behaviour: many opportunities, high rate.
    goal_se = standard_error(CHANCE_QUALITY, SHOTS)
    press_opportunities = 700
    press_rate = 0.30
    press_se = standard_error(press_rate, press_opportunities)

    rows = [
        ("goals from shots", SHOTS, CHANCE_QUALITY, goal_se),
        ("presses from chances to press", press_opportunities, press_rate, press_se),
    ]
    print("  measurement                      n     rate     SE      relative SE")
    for label, n, rate, se in rows:
        print(f"  {label:<30} {n:>5}   {rate:>5.3f}  {se:.4f}   {se / rate:>7.1%}")

    print()
    ratio = (goal_se / CHANCE_QUALITY) / (press_se / press_rate)
    print(f"The behaviour measurement is about {ratio:.0f}x more precise, in")
    print("relative terms, from the same single season of football.")
    print()
    print("Two reasons, both visible in the formula:")
    print("  - many more opportunities (n is 700, not 25)")
    print("  - a much higher rate, so less relative wobble")
    print()
    print("This is the statistical argument for the whole project. How often a")
    print("player presses, drops deep, or gets into the box stabilises within a")
    print("season. Whether his shots went in does not. So if you want to know")
    print("what a transfer changed, measure the behaviour, not the goals.")


def main() -> None:
    print("=" * 72)
    print("LESSON 01 - SAMPLING VARIANCE")
    print("=" * 72)
    part_one_the_setup()
    part_two_the_distribution()
    part_three_how_many_shots()
    part_four_why_behaviour_is_different()
    rule("Check it yourself")
    print("With p = 0.144 and n = 25:")
    print("  P(0) = 0.856**25                  = 0.0205")
    print("  P(1) = 25 * 0.144 * 0.856**24     = 0.0862")
    print("  P(0 or 1)                         = 0.1067")
    print()
    print("Next: learning/02_distance_metrics.py")


if __name__ == "__main__":
    main()
