from unittest import TestCase

import pandas as pd


class TestCommon(TestCase):
    def test_combine_data_horizontal(self):
        df_left = pd.DataFrame(
            {"Name": ["A", "B", "C"], "Pos": ["RB", "WR", "QB"], "Pts": range(3)}
        )
        assert len(df_left) == 3
