# learning/

Worked examples for understanding the statistics behind Carryover.

These are not tests and not part of the package. Each lesson is a standalone
script that narrates its own arithmetic as it runs, so that reading the output
and reading the source teach the same thing. Every number is hand-checkable on
paper, which is the point: PRD section 23 requires a manual example for
analytical logic, and these are where that habit gets built.

```sh
make learn                                  # run every lesson in order
.venv/bin/python learning/01_sampling_variance.py   # or one at a time
```

Standard library only. No numpy, no pandas. Anything you cannot follow line by
line is not teaching you much.

## Lessons

| # | Lesson | Concept | Why it matters here |
|---|---|---|---|
| 01 | `01_sampling_variance.py` | Binomial variance, standard error | Why one season of goals is nearly uninformative, and why behaviour is not |
| 02 | `02_distance_metrics.py` | L1, L2, cosine distance | What `role_transition_distance` actually computes, and why cosine would be wrong |

## A note on the numbers in lesson 01

The shot profile used (25 shots, 3.6 expected goals, 1 goal) is a realistic
striker season and is deliberately **not** attached to a named player.

PRD section 7.8 holds Openda to Juventus and David to Juventus as final
holdouts. Using arithmetic to illustrate binomial variance does not
reverse-engineer any feature or threshold, but keeping the case anonymous in
teaching material costs nothing and keeps the holdout discipline visibly intact.
Treat that as part of the lesson.

## Planned next

- **03** Percentiles vs z-scores, and why "percentile against whom" changes everything
- **04** Regression to the mean, the single biggest driver of apparent transfer flops
- **05** Split-half reliability and Mean Reciprocal Rank, the B1 benchmark rung
- **06** NMF on a toy heatmap, the technique behind Player Vectors and StatsBomb style
