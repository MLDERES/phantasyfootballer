import pandas as pd
import pytest
from phantasyfootballer.io import RemotePartitionedDataSet
from .conftest import TEST_DATA_FOLDER
from phantasyfootballer.common import NFL_SEASON

TEST_SEASON_RESULTS_FOLDER = TEST_DATA_FOLDER / "results/season_long"
TEST_WEEKLY_RESULTS_FOLDER = TEST_DATA_FOLDER / "results/weekly"


class MockFootball_db:
    def __init__(self):
        pass

    def get_stats(self, year: int, week: int) -> pd.DataFrame:
        if week == NFL_SEASON:
            return pd.read_csv(TEST_SEASON_RESULTS_FOLDER / "2018.csv")
        else:
            return pd.read_csv(TEST_WEEKLY_RESULTS_FOLDER / "2019/week1.csv")

    def get_stats_for_position(
        self, position: str, year: int, week: int
    ) -> pd.DataFrame:
        return self.get_stats(year, week)


class TestDataCatalog:
    date_range_past_seasons = {
        "start_date": {"week": NFL_SEASON, "year": 2018},
        "end_date": {"week": NFL_SEASON, "year": 2019},
    }

    date_range_future_seasons = {
        "start_date": {"week": NFL_SEASON, "year": 2020},
        "end_date": {"week": NFL_SEASON, "year": 2021},
    }

    date_range_past_weeks = {
        "start_date": {"week": 1, "year": 2018},
        "end_date": {"week": 10, "year": 2019},
    }
    date_range_future_weeks = {
        "start_date": {"week": 11, "year": 2020},
        "end_date": {"week": 17, "year": 2021},
    }

    @pytest.fixture
    def results_weekly_raw(self, data_catalog):
        return data_catalog.load("results.weekly.raw")

    @pytest.fixture
    def data_catalog(self, project_context):
        assert project_context, "Nothing loaded"
        return project_context.catalog

    @pytest.fixture
    def dataset(self):
        return RemotePartitionedDataSet(
            str(TEST_WEEKLY_RESULTS_FOLDER),
            dataset="pandas.CSVDataSet",
            remote_data_source=MockFootball_db.get_stats,
            date_range_type=None,
        )

    @pytest.fixture
    def past_weekly_results_dataset(self):
        return RemotePartitionedDataSet(
            str(TEST_WEEKLY_RESULTS_FOLDER),
            dataset="pandas.CSVDataSet",
            remote_data_source=MockFootball_db.get_stats,
            date_range_type="past_weeks",
        )

    @pytest.fixture
    def past_season_results_dataset(self):
        return RemotePartitionedDataSet(
            str(TEST_SEASON_RESULTS_FOLDER),
            dataset="pandas.CSVDataSet",
            remote_data_source=MockFootball_db.get_stats,
            date_range_type="past_seasons",
        )

    @pytest.fixture
    def future_season_results_dataset(self):
        return RemotePartitionedDataSet(
            str(TEST_SEASON_RESULTS_FOLDER),
            dataset="pandas.CSVDataSet",
            remote_data_source=MockFootball_db.get_stats,
            date_range_type="future_seasons",
        )

    @pytest.fixture
    def future_weeks_results_dataset(self):
        return RemotePartitionedDataSet(
            str(TEST_SEASON_RESULTS_FOLDER),
            dataset="pandas.CSVDataSet",
            remote_data_source=MockFootball_db.get_stats,
            date_range_type="future_weeks",
        )

    def test_load_remotepartitioneddataset(self, results_weekly_raw):
        assert results_weekly_raw, "Loading `results.weekly.raw` failed"

    @pytest.mark.parametrize(
        "date_range, expected_partition",
        [
            (date_range_future_weeks, "2020/week11"),
            (date_range_future_weeks, "2021/week10"),
            #     [, "2021/week10", pytest.param("2000", marks=pytest.mark.xfail)],
            # ),
            # (
            #     date_range_future_seasons,
            #     ["2020", "2021", pytest.param("2000", marks=pytest.mark.xfail)],
            # ),
            # (
            #     date_range_past_seasons,
            #     ["2018", "2019", pytest.param("2000", marks=pytest.mark.xfail)],
            # ),
            # (
            #     date_range_past_weeks,
            #     ["2018/week2", "2019/week6", pytest.param("2019/week11", marks=pytest.mark.xfail)],
            # ),
        ],
    )
    def test_gen_requested_partitions(self, dataset, date_range, expected_partition):
        partitions = dataset._gen_requested_partitions(date_range)
        assert expected_partition in partitions

    # @pytest.mark.parametrize(
    #     "expected_partition",
    #     ["2020/week10", "2020/week11", pytest.param("2000/week1", marks=pytest.mark.xfail),],
    # )
    # def test_gen_requested_partitions_past_weeks(
    #     self, past_weekly_results_dataset, expected_partition
    # ):
    #     assert past_weekly_results_dataset
    #     partitions = past_weekly_results_dataset._gen_requested_partitions(
    #         self.date_range_past_weeks
    #     )
    #     assert expected_partition in partitions

    # @pytest.mark.parametrize(
    #     "expected_partition", ["2020", "2021", pytest.param("2025", marks=pytest.mark.xfail)],
    # )
    # def test_gen_requested_partitions_forward_season(
    #     self, future_season_results_dataset, expected_partition
    # ):
    #     assert future_season_results_dataset
    #     partitions = future_season_results_dataset._gen_requested_partitions(
    #         self.date_range_future_seasons
    #     )
    #     assert expected_partition in partitions

    # @pytest.mark.parametrize(
    #     "expected_partition",
    #     ["2010/week1", "2020/week2", pytest.param("2025/week10", marks=pytest.mark.xfail),],
    # )
    # def test_gen_requested_partitions_past_season(
    #     self, past_season_results_dataset, expected_partition
    # ):
    #     assert past_season_results_dataset
    #     partitions = past_season_results_dataset._gen_requested_partitions(
    #         self.date_range_past_seasons
    #     )
    #     assert expected_partition in partitions

    def test_get_missing_data(self, past_weekly_results_dataset):
        results = past_weekly_results_dataset._get_missing_data(
            years=[2018, 2019], weeks=[1, 10]
        )
        assert results
        assert "2018/week1" in results.keys()
        assert "2018/week10" in results.keys()
        assert "2019/week1" in results.keys()
        assert "2019/week10" in results.keys()
        assert type(results["2018/week1"]) == pd.DataFrame
        assert type(results["2019/week10"]) == pd.DataFrame
