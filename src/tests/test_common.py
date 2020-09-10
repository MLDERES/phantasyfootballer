import pandas as pd
import pytest

from phantasyfootballer.io.CachedRemoteCSVDataSet import CachedRemoteCSVDataSet as cds
from phantasyfootballer.common import NFLDate


def test_combine_data_horizontal():
    df_left = pd.DataFrame(
        {"Name": ["A", "B", "C"], "Pos": ["RB", "WR", "QB"], "Pts": range(3)}
    )
    assert len(df_left) == 3


expiration_testdata = [
    ("8h", 8),
    ("8H", 8),
    ("08 H", 8),
    ("12  h", 12),
    ("60M", 1),
    ("120M", 2),
    ("1 D", 24),
]


@pytest.mark.parametrize("test_input, expected", expiration_testdata)
def test_calculate_expiration(test_input, expected):
    result = cds._calculate_expiration_hours(test_input)
    assert result == expected


nfl_testdates = [("2020-09-09", 2020, 1), ("2020-10-10", 2020, 5)]


@pytest.mark.parametrize("test_input, expected_year, expected_week", nfl_testdates)
def test_nfldate(test_input, expected_year, expected_week):
    result = NFLDate(test_input)
    result_year, result_week = result.week, result.year
    assert result_year == expected_year
    assert result_week == expected_week
