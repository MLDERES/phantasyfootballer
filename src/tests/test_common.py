import pandas as pd
import pytest

from phantasyfootballer.common import NFLDate
from phantasyfootballer.io.CachedRemoteCSVDataSet import CachedRemoteCSVDataSet as cds


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

    nfl_next_dates = [
        ("2020-09-09", (2020, 1), (2020, 2), (2019, 17)),  # Week 1, Tues,
        ("2020-10-10", (2020, 5), (2020, 6), (2020, 4)),  # Week 5, Saturday
        ("2020-12-2", (2020, 13), (2020, 14), (2020, 12)),  # Week 13, Wed
        ("2020-09-14", (2020, 1), (2020, 2), (2019, 17)),  # Week 1, Monday
        ("2021-01-02", (2020, 17), (2021, 1), (2020, 16)),  # Week 17, Fri
        (
            "2021-02-20",
            (2020, 0),
            (2021, 0),
            (2019, 0),
        ),  # After the season, but in 2020
        ("2020-08-01", (2020, 0), (2021, 0), (2019, 0)),  # Before season in 2020
    ]

    @pytest.mark.parametrize("test_input, expected_year, expected_week", nfl_testdates)
    def test_nfldate(self, test_input, expected_year, expected_week):
        # breakpoint()
        result = NFLDate(test_input)
        result_year, result_week = result.year, result.week
        assert result_year == expected_year
        assert result_week == expected_week

    @pytest.fixture(scope="function")
    def forward_dates(self, request):
        return (request.param[3], request.param[4])
        # return (request.param['next_season'], request.param['next_week'])

    @pytest.mark.parametrize(
        "test_input, expected, expected_next, expected_prev", nfl_next_dates
    )
    def test_nfldate_next_week(
        self, test_input, expected, expected_next, expected_prev
    ):
        result = NFLDate(test_input)
        result_year, result_week = result.year, result.week
        assert result_year == expected[0]
        assert result_week == expected[1]
        next_week = NFLDate.next_week(result)
        next_expected = NFLDate(year=expected_next[0], week=expected_next[1])
        assert next_week.year == next_expected.year
        assert next_week.week == next_expected.week
        prev_week = NFLDate.prev_week(result)
        prev_expected = NFLDate(year=expected_prev[0], week=expected_prev[1])
        assert prev_week.year == prev_expected.year
        assert prev_week.week == prev_expected.week

    @pytest.mark.parametrize(
        "test_input, expected, expected_next, expected_prev", nfl_next_dates
    )
    def test_nfldate_cmp(self, test_input, expected, expected_next, expected_prev):
        base_date = NFLDate(test_input)
        this_week = NFLDate(year=expected[0], week=expected[1])
        next_week = NFLDate(year=expected_next[0], week=expected_next[1])
        last_week = NFLDate(year=expected_prev[0], week=expected_prev[1])
        assert base_date == this_week, "failed eq"
        assert base_date < next_week, "failed lt"
        assert base_date <= next_week, "failed lte"
        assert base_date > last_week, "failed gt"
        assert base_date >= last_week, "failed gte"
