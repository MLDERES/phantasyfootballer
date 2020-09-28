import pandas as pd
import pandas.testing as pdt
import pytest

from kedro.pipeline import Pipeline

import phantasyfootballer.pipelines.data_import as di
from phantasyfootballer.pipelines.data_import.nodes import (
    _create_player_merge_name,
    _replace_player_name,
    average_stats_by_player,
    fixup_player_names,
    split_year_from_week,
)
from phantasyfootballer.settings import MERGE_NAME, PLAYER_NAME, Stats
from phantasyfootballer.common import NFL_SEASON
from phantasyfootballer.common_nodes import drop_unknown_columns


@pytest.fixture
def mergename_test_data():
    return


class Test_Nodes:
    def test_replace_player_name(self):
        assert _replace_player_name("Gardner Minshew II") == "Gardner Minshew"
        assert _replace_player_name("Michael D") == "Michael D"

    def test_fixup_player_name(self):
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
                MERGE_NAME: [
                    "gardnerminshew",
                    "michaeld",
                    "bennystill",
                    "michaelpittman",
                ],
            }
        )
        result = fixup_player_names(test_frame)
        pdt.assert_frame_equal(result, expected_frame)

    @pytest.mark.parametrize(
        "test_input, expected",
        [
            ("Billy Van Heusen", "billyvanheusen"),
            ("R. Jay Soward", "rjaysoward"),
            ("Brad St. Louis", "bradstlouis"),
            ("Chris Fuamatu-Ma'afala", "chrisfuamatumaafala"),
            ("Donnie Joe Morris", "donniejoemorris"),
            ("Christian McCaffery", "christianmccaffery"),
        ],
    )
    def test_player_mergename(self, test_input, expected):
        result = _create_player_merge_name(test_input)
        assert result == expected

    def test_split_year_from_week(self):
        test_frame = pd.DataFrame(
            {
                Stats.YEAR: ["1999/week1", "2010/week10"],
                Stats.NFL_WEEK: [NFL_SEASON, NFL_SEASON],
            }
        )
        result = split_year_from_week(test_frame)
        expected_frame = pd.DataFrame(
            {Stats.YEAR: ["1999", "2010"], Stats.NFL_WEEK: [1, 10]}
        )
        pdt.assert_frame_equal(result, expected_frame)

    @pytest.fixture
    def partitioned_data_pandas(self):
        keys = ("p1/data1.csv", "p2.csv", "p1/data2.csv", "p3", "_p4")
        return {
            k: pd.DataFrame({"part": k, "counter": list(range(counter))})
            for counter, k in enumerate(keys, 1)
        }

    def test_create_partitions(self, partitioned_data_pandas):
        average_stats_by_player(partitioned_data_pandas)
        pass

    def test_drop_unknown_columns(self):
        df = pd.DataFrame({"Unnamed: 0": range(5), "A": range(5)})
        result_df = drop_unknown_columns(df)
        pdt.assert_frame_equal(result_df, pd.DataFrame({"A": range(5)}))


class Test_Pipelines:
    def test_create_annual_projections_pipeline(self):
        pipeline = di.create_annual_projections_pipeline()
        assert isinstance(pipeline, Pipeline)
        assert any(pipeline.nodes)

    def test_create_annual_results_pipeline(self):
        pipeline = di.create_annual_results_pipeline()
        assert isinstance(pipeline, Pipeline)
        assert any(pipeline.nodes)

    def test_create_weekly_results_pipeline(self):
        pipeline = di.create_weekly_results_pipeline(start_date="", end_date="")
        assert isinstance(pipeline, Pipeline)
        assert any(pipeline.nodes)

    # TODO: ISSUE 41: Configurable results pipeline
    # def test_create_weekly_projections_pipeline(self):
    #     pipeline = di.create_weekly_projections_pipeline()
    #     assert isinstance(pipeline, Pipeline)
    #     assert any(pipeline.nodes)


if __name__ == "__main__":
    pass
