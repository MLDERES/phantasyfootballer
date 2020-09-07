import pytest

import pandas as pd
import pandas.testing as pdt
from phantasyfootballer.common import PLAYER_NAME, MERGE_NAME, Stats, NFL_WEEK_ALL
from phantasyfootballer.pipelines.data_import.nodes import (
    _replace_player_name,
    fixup_player_names,
    _create_player_merge_name,
    split_year_from_week,
    average_stats_by_player,
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


def test_split_year_from_week():
    test_frame = pd.DataFrame(
        {
            Stats.YEAR: ["1999/week1", "2010/week10"],
            Stats.NFL_WEEK: [NFL_WEEK_ALL, NFL_WEEK_ALL],
        }
    )
    result = split_year_from_week(test_frame)
    expected_frame = pd.DataFrame(
        {Stats.YEAR: ["1999", "2010"], Stats.NFL_WEEK: [1, 10]}
    )
    pdt.assert_frame_equal(result, expected_frame)


@pytest.fixture
def partitioned_data_pandas():
    keys = ("p1/data1.csv", "p2.csv", "p1/data2.csv", "p3", "_p4")
    return {
        k: pd.DataFrame({"part": k, "counter": list(range(counter))})
        for counter, k in enumerate(keys, 1)
    }


def test_create_partitions(partitioned_data_pandas):
    average_stats_by_player(partitioned_data_pandas)
    pass


if __name__ == "__main__":
    test_split_year_from_week()
