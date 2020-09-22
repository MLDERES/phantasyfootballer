# from datetime import date
# import importlib
# import logging
# import os
# import re
# from pathlib import Path
# from typing import Any, Callable, Dict, List, Union, Type, Optional
# import pandas as pd
# from phantasyfootballer.common import (
#     NFLDate,
#     NFL_ALL_WEEKS,
#     NFL_SEASON,
#     CURRENT_NFL_YEAR,
#     CURRENT_NFL_WEEK,
#     EARLIEST_NFL_YEAR,
# )

# from kedro.io import PartitionedDataSet, DataSetError, AbstractDataSet

# logger = logging.getLogger("phantasyfootballer.io")
# DEBUG = logger.debug
# INFO = logger.info

# MODULE_SEPARATOR = "."
# CURRENT_NFL_WEEK = NFLDate(date.today()).week
# CURRENT_NFL_YEAR = NFLDate(date.today()).year
# LAST_WEEK_SEASON = CURRENT_NFL_YEAR.total_weeks()


# DATE_RANGE_TYPE: Dict[str, Dict[str, str]] = {
#     "future_season": {
#         "start_date": {"week": NFL_SEASON, "year": CURRENT_NFL_YEAR},
#         "end_date": {"week": NFL_SEASON, "year": CURRENT_NFL_YEAR},
#     },
#     "future_weeks": {
#         "start_date": {"week": CURRENT_NFL_WEEK, "year": CURRENT_NFL_YEAR},
#         "end_date": {"week": LAST_WEEK_SEASON, "year": CURRENT_NFL_YEAR},
#     },
#     "past_weeks": {
#         "start_date": {"week": 1, "year": EARLIEST_NFL_YEAR},
#         "end_date": {"week": CURRENT_NFL_WEEK, "year": CURRENT_NFL_YEAR},
#     },
#     "past_seasons": {
#         "start_date": {"week": NFL_SEASON, "year": EARLIEST_NFL_YEAR},
#         "end_date": {"week": NFL_SEASON, "year": CURRENT_NFL_YEAR},
#     },
# }


# class CSVCombineWeekly(AbstractDataSet):
#     """
#     Creates a set of files, by year for each week of the season.

#     NOTES:
#     ------

#     """

#     def __init__(
#         self,
#         path: str,
#         remote_data_source: Union[Callable, str],
#         filepath_arg: str = "filepath",
#         filename_suffix: str = "",
#         date_range_type: Optional[str] = None,
#         **load_kwargs,
#     ):
#         """Instantiate a CSVIncrementalDataSet object.

#         Params
#         ------
#         data_source: Callable or str
#             Should be a function that is used to get the latest version of the file from a remote source


#         """
#         # self._data_source_kwargs = load_kwargs

#         # self._local_filepath = Path(local_source_filepath)

#         # if callable(remote_data_source):
#         #     DEBUG(f"CSVCombineWeekly: callable {remote_data_source=}")
#         #     self.data_source = data_source
#         # else:
#         #     DEBUG(f"CSVCombineWeekly: string {remote_data_source=}")
#         #     path_parts = remote_data_source.split(MODULE_SEPARATOR)
#         #     function_name = path_parts[-1]
#         #     module_path = MODULE_SEPARATOR.join(path_parts[:-1])
#         #     module = importlib.import_module(module_path)
#         #     self.remote_data_source = getattr(module, function_name)

#     def _load(self) -> Dict[str, Callable[[], Any]]:
#         """
#         This function will look to either the local datasource or to the web for the
#         requested data.  If the dates requested aren't available, then we'll go to the web and pick them up
#         """

#         partitions = {}

#         """ Request is Seasons:
#                 Request is for current season
#                     If we are currently in season
#                         if the file is more than a week old
#                             make a request
#                         else
#                             add file to the list of partitions
#                     else if we are out of season
#                         then if the file is there
#                             add to the list of partitions to offer
#                         else
#                             make a request to find the data


#                 if date request is for seasons then
#                 comb the directory provided for seasonal data.

#         """

#         return partitions

#     def _partition_to_path(self, path: str):
#         dir_path = self._path.rstrip(self._sep)
#         path = path.lstrip(self._sep)
#         full_path = self._sep.join([dir_path, path]) + self._filename_suffix
#         return full_path

#     def _path_to_partition(self, path: str) -> str:
#         dir_path = self._filesystem._strip_protocol(self._normalized_path)
#         path = path.split(dir_path, 1).pop().lstrip(self._sep)
#         if self._filename_suffix and path.endswith(self._filename_suffix):
#             path = path[: -len(self._filename_suffix)]
#         return path

#     def _save(self, data: pd.DataFrame) -> None:
#         pass

#     def _describe(self):
#         return self._data_source_kwargs

#     @staticmethod
#     def _validate_date_range_type(date_range_type: Optional[str]) -> None:
#         assert date_range_type is None or date_range_type in DATE_RANGE_TYPE.keys(), (
#             "Argument date_range_type must be None or one of "
#             f"{DATE_RANGE_TYPE.keys()}, but {date_range_type} was received."
#         )
