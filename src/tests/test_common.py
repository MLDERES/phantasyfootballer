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


class TestNFL_Date:

    nfl_testdates = [
        ("2020-09-09", 2020, 1),  # Week 1, Tues,
        ("2020-10-10", 2020, 5),  # Week 5, Saturday
        ("2020-12-2", 2020, 13),  # Week 13, Wed
        ("2020-09-14", 2020, 1),  # Week 1, Monday
        ("2021-01-02", 2020, 17),  # Week 17, Fri
        ("2021-02-20", 2020, 0),  # After the season, but in 2020
        ("2020-08-01", 2020, 0),  # Before season in 2020
        ("2020-08-20", 2020, -2),  # Pre-season, week #2
        ("2020-08-27", 2020, -3),  # Pre-season, week #3
    ]

    @pytest.mark.parametrize("test_input, expected_year, expected_week", nfl_testdates)
    def test_nfldate(self, test_input, expected_year, expected_week):
        # breakpoint()
        result = NFLDate(test_input)
        result_year, result_week = result.year, result.week
        assert result_year == expected_year
        assert result_week == expected_week
