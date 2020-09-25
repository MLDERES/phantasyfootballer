import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Union, Type, Optional, Tuple
import pandas as pd
from phantasyfootballer.common import (
    NFLDate,
    NFL_SEASON,
    EARLIEST_NFL_YEAR,
)

from kedro.io import PartitionedDataSet, DataSetError, AbstractDataSet
from datetime import date
import importlib

logger = logging.getLogger("phantasyfootballer.io")
DEBUG = logger.debug
INFO = logger.info

MODULE_SEPARATOR = "."
NFL_TODAY = NFLDate(date.today())
CURRENT_NFL_WEEK = NFL_TODAY.week
CURRENT_NFL_YEAR = NFL_TODAY.year
LAST_WEEK_SEASON = NFL_TODAY.total_weeks

DATE_RANGE_TYPE = {
    "future_seasons": {
        "start_date": {"week": NFL_SEASON, "year": CURRENT_NFL_YEAR},
        "end_date": {"week": NFL_SEASON, "year": CURRENT_NFL_YEAR},
    },
    "future_weeks": {
        "start_date": {"week": CURRENT_NFL_WEEK, "year": CURRENT_NFL_YEAR},
        "end_date": {"week": LAST_WEEK_SEASON, "year": CURRENT_NFL_YEAR},
    },
    "past_weeks": {
        "start_date": {"week": 1, "year": EARLIEST_NFL_YEAR},
        "end_date": {"week": CURRENT_NFL_WEEK, "year": CURRENT_NFL_YEAR},
    },
    "past_seasons": {
        "start_date": {"week": NFL_SEASON, "year": EARLIEST_NFL_YEAR},
        "end_date": {"week": NFL_SEASON, "year": CURRENT_NFL_YEAR},
    },
}


class RemotePartitionedDataSet(PartitionedDataSet):
    """
    Creates a set of files, by year for each week of the season.

    NOTES:
    ------

    """

    def __init__(
        self,
        path: str,
        dataset: Union[str, Type[AbstractDataSet], Dict[str, Any]],
        remote_data_source: Union[Callable, str],
        date_range_type: Optional[str] = None,
        filepath_arg: str = "filepath",
        filename_suffix: str = ".csv",
        load_args: Dict[str, Any] = None,
        save_args: Dict[str, Any] = None,
        *kwargs,
    ):
        super().__init__(
            path=path,
            dataset=dataset,
            filepath_arg=filepath_arg,
            filename_suffix=filename_suffix,
        )

        self._validate_date_range_type(date_range_type)
        self._date_range = (
            {} if date_range_type is None else DATE_RANGE_TYPE[date_range_type]
        )

        if callable(remote_data_source):
            self._remote_data_source = remote_data_source
        else:
            DEBUG(f"CSVCombineWeekly: string {remote_data_source=}")
            path_parts = remote_data_source.split(MODULE_SEPARATOR)
            function_name = path_parts[-1]
            module_path = MODULE_SEPARATOR.join(path_parts[:-1])
            module = importlib.import_module(module_path)
            self._remote_data_source = getattr(module, function_name)

        self._load_args = {} if load_args is None else load_args
        self._save_args = {} if save_args is None else save_args

    def _load(self) -> Dict[str, Callable[[], Any]]:
        """
        This function will look to either the local datasource or to the web for the
        requested data.  If the dates requested aren't available, then we'll go to the web and pick them up
        """
        partitions = super()._load()
        DEBUG(f"Found {len(partitions)} partitions in")
        # DEBUG(f'Some of the partitions {[x,y for x, y in partitions]}')
        if not partitions:
            raise DataSetError("No partitions found in `{}`".format(self._path))

        # The partitions we have
        existing_partitions = {_ for _ in partitions.keys()}
        seasons_requested = self._gen_requested_partitions(self._date_range)
        missing_partitions = set(seasons_requested.keys()) - existing_partitions

        missing_years = list({seasons_requested[y][0] for y in missing_partitions})
        missing_weeks = list({seasons_requested[w][1] for w in missing_partitions})
        missing_data = self._get_missing_data(missing_years, missing_weeks)
        self._stash_missing_data(missing_data)

        # This is a hack - requring a second reload of the data, but it might be worth it
        partitions = super()._load()
        return partitions

    def _gen_requested_partitions(
        self, date_range: Dict[str, Dict[str, int]]
    ) -> Dict[str, Tuple[int, int]]:
        """
        Create a partition key and tuple combination of year, week based on the date range
        """
        start_year, end_year = (
            date_range["start_date"]["year"],
            date_range["end_date"]["year"],
        )
        start_year, end_year = min(start_year, end_year), max(start_year, end_year)
        start_week, end_week = (
            date_range["start_date"]["week"],
            date_range["end_date"]["week"],
        )
        start_week, end_week = min(start_week, end_week), max(start_week, end_week)
        if start_week == NFL_SEASON:
            retVal = {f"{y}": (y, NFL_SEASON) for y in range(start_year, end_year + 1)}
        else:
            retVal = {
                f"{y}/week{w}": (y, w)
                for y in range(start_year, end_year + 1)
                for w in range(start_week, end_week + 1)
            }
            # Since we are crossing years, we need to add in weeks between the end of one year and the begining of the next
            if start_year != end_year:
                retVal.update(
                    {
                        f"{y}/week{w}": (y, w)
                        for y in range(start_year + 1, end_year + 1)
                        for w in range(1, end_week)
                    }
                )
        return retVal

    def _get_missing_data(self, years: List[int], weeks: List[int]) -> Dict[str, Any]:
        """
        Gather data for every week and year combination provided

        Parameters
        ----------
        years - List[int]
            Every season for which data ought to be collected
        weeks - List[int]
            All the weeks of each season that should be collected.  If this value is `NFL_SEASON` then only aggregated season long data will be collected.
            If this value is
        """
        missing_data = {}
        season_data_only = weeks[0] == NFL_SEASON
        for y in years:
            if season_data_only:
                missing_data[f"{y}"] = self._remote_data_source(year=y, week=NFL_SEASON)
            else:
                for w in weeks:
                    partition = f"{y}/week{w}"
                    missing_data[partition] = self._remote_data_source(year=y, week=w)
        return missing_data

    def _stash_missing_data(self, data: Dict[str, Any]) -> None:
        for partition_id, part_data in sorted(data.items()):
            # NEXT: need to decide if we have a directory and a filename
            #       If it has a directory, then we need to ensure the dir is there
            #       then we can start dumping the files in there
            if part_data:
                path = Path(super()._partition_to_path(partition_id))
                DEBUG(f"stash missing data on {path}")
                path.parent.mkdir(parents=True, exist_ok=True)
                part_data.to_csv(path, **self._save_args)

    def _save(self, data: pd.DataFrame) -> None:
        pass

    def _describe(self):
        return {**self._save_args, **self._load_args}

    @staticmethod
    def _validate_date_range_type(date_range_type: Optional[str]) -> None:
        assert date_range_type is None or date_range_type in DATE_RANGE_TYPE.keys(), (
            "Argument date_range_type must be None or one of "
            f"{DATE_RANGE_TYPE.keys()}, but {date_range_type} was received."
        )


if __name__ == "__main__":

    pass