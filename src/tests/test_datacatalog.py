import pandas as pd
import pytest
from phantasyfootballer.io import RemotePartitionedDataSet
from .conftest import TEST_DATA_FOLDER
from phantasyfootballer.common import NFL_SEASON
from shutil import copytree

SEASON_RESULTS_DIR = "results/season_long"
WEEKLY_RESULTS_DIR = "results/weekly"
TEST_SEASON_RESULTS_FOLDER = TEST_DATA_FOLDER / SEASON_RESULTS_DIR
TEST_WEEKLY_RESULTS_FOLDER = TEST_DATA_FOLDER / WEEKLY_RESULTS_DIR


class MockFootball_db:
    def __init__(self):
        pass

    @staticmethod
    def get_stats(year: int, week: int) -> pd.DataFrame:
        if week == NFL_SEASON:
            return pd.read_csv(TEST_SEASON_RESULTS_FOLDER / "2018.csv")
        else:
            return pd.read_csv(TEST_WEEKLY_RESULTS_FOLDER / "2019/week1.csv")

    @staticmethod
    def get_stats_for_position(position: str, year: int, week: int) -> pd.DataFrame:
        return MockFootball_db.get_stats(year, week)


@pytest.fixture
def remote_part_dataset(request, tmp_path):
    date_range_type = request.param
    data_path = SEASON_RESULTS_DIR
    if date_range_type:
        data_path = (
            SEASON_RESULTS_DIR if "season" in date_range_type else WEEKLY_RESULTS_DIR
        )
        rpds = RemotePartitionedDataSet(
            path=str(tmp_path / data_path),
            dataset="pandas.CSVDataSet",
            remote_data_source=MockFootball_db.get_stats,
            date_range_type=date_range_type,
        )
    else:
        rpds = RemotePartitionedDataSet(
            str(tmp_path / data_path),
            dataset="pandas.CSVDataSet",
            remote_data_source=MockFootball_db.get_stats,
            date_range_type=None,
        )

    copytree(TEST_DATA_FOLDER / data_path, tmp_path / data_path)
    yield rpds


class TestDataCatalog:
    date_range_past_seasons = {
        "start_date": {"week": NFL_SEASON, "year": 2018},
        "end_date": {"week": NFL_SEASON, "year": 2019},
    }

    date_range_future_seasons = {
        "start_date": {"week": NFL_SEASON, "year": 2020},
        "end_date": {"week": NFL_SEASON, "year": 2025},
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

    @pytest.mark.parametrize(
        "remote_part_dataset, partition",
        [
            ("future_seasons", "2020"),
            ("past_seasons", "2019"),
            ("future_weeks", "2020/week11"),
            ("past_weeks", "2019/week5"),
            pytest.param(
                "future_weeks",
                "2019/week5",
                marks=pytest.mark.xfail(reason="not in the future"),
            ),
        ],
        indirect=["remote_part_dataset"],
    )
    def test_load_remotepartitioneddataset(self, remote_part_dataset, partition):
        assert remote_part_dataset, "Construction of RemotePartitionedDataSet failed"
        partitions = remote_part_dataset._load()
        assert partitions, "Load of RemotePartitionedDataSet failed"
        assert partition in partitions, "Expected partition missing"

    @pytest.mark.parametrize(
        "date_range, expected_partition",
        [
            (date_range_future_weeks, "2020/week11"),
            (date_range_future_weeks, "2021/week10"),
            pytest.param(
                date_range_future_weeks,
                "2021",
                marks=pytest.mark.xfail(reason="passing season to a week range"),
            ),
            (date_range_future_seasons, "2020"),
            (date_range_future_seasons, "2021"),
            (date_range_future_seasons, "2025"),
            pytest.param(
                date_range_future_seasons,
                "2026",
                marks=pytest.mark.xfail(reason="too far in the future"),
            ),
            pytest.param(
                date_range_future_seasons,
                "2020/week11",
                marks=pytest.mark.xfail(
                    reason="passing a week, expecting season partition"
                ),
            ),
            (date_range_past_seasons, "2018"),
            (date_range_past_weeks, "2019/week10"),
            (date_range_past_weeks, "2019/week9"),
        ],
    )
    def test_gen_requested_partitions(self, dataset, date_range, expected_partition):
        partitions = dataset._gen_requested_partitions(date_range)
        assert expected_partition in partitions

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
