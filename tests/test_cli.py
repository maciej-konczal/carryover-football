from pathlib import Path

from carryover_football.cli import main

PROJECT_ROOT = Path(__file__).parents[1]
ORIGIN = PROJECT_ROOT / "examples/data/synthetic_origin_role.json"
DESTINATION = PROJECT_ROOT / "examples/data/synthetic_destination_role.json"


def test_cli_reports_required_role_transition_information(capsys) -> None:
    exit_code = main([str(ORIGIN), str(DESTINATION)])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Two largest new demands:" in output
    assert "pressing: +0.25" in output
    assert "link_play: +0.24" in output
    assert "Two most de-emphasized behaviors:" in output
    assert "aerial_play: -0.09" in output
    assert "box_presence: -0.07" in output
    assert "Overall role-transition distance: 0.148" in output
    assert "NOT A PROBABILITY" in output
    assert "RISK PERCENTAGE" in output
    assert "OR PREDICTION" in output
