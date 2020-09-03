import pytest

import pandas as pd
import pandas.testing as pdt
from phantasyfootballer.common import PLAYER_NAME, MERGE_NAME
from phantasyfootballer.pipelines.data_import.nodes import (
    _replace_player_name,
    fixup_player_names,
    _create_player_merge_name,
)


def test_replace_player_name():
    assert _replace_player_name("Gardner Minshew II") == "Gardner Minshew"
    assert _replace_player_name("Michael D") == "Michael D"


def test_fixup_player_name():
    test_frame = pd.DataFrame(
        {
            PLAYER_NAME: [
                "Gardner Minshew II",
                "Michael D",
                "Benny Still Jr.",
                "Michael Pittman Jr.",
            ]
        }
    )
    expected_frame = pd.DataFrame(
        {
            PLAYER_NAME: [
                "Gardner Minshew",
                "Michael D",
                "Benny Still",
                "Michael Pittman",
            ],
            MERGE_NAME: ["gardnerminshew", "michaeld", "bennystill", "michaelpittman"],
        }
    )
    result = fixup_player_names(test_frame)
    pdt.assert_frame_equal(result, expected_frame)


mergename_test_data = [
    ("Billy Van Heusen", "billyvanheusen"),
    ("R. Jay Soward", "rjaysoward"),
    ("Brad St. Louis", "bradstlouis"),
    ("Chris Fuamatu-Ma'afala", "chrisfuamatumaafala"),
    ("Donnie Joe Morris", "donniejoemorris"),
    ("Christian McCaffery", "christianmccaffery"),
]


@pytest.mark.parametrize("test_input, expected", mergename_test_data)
def test_player_mergename(test_input, expected):
    result = _create_player_merge_name(test_input)
    assert result == expected


if __name__ == "__main__":
    test_fixup_player_name()
