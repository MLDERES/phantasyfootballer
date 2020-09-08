import pandas as pd
import pytest

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
