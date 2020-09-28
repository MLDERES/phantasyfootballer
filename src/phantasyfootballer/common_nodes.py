import logging
from typing import Any, Callable, Dict, Sequence, Union
import pandas as pd

from .settings import Stats
from .common import NFL_SEASON

logger = logging.getLogger("phantasyfootballer")
DEBUG = logger.debug
INFO = logger.info


def create_partitions(
    partition_keys: Union[Sequence[str], Any], *data_frames: pd.DataFrame
) -> Dict[Any, pd.DataFrame]:
    """
    Create a set of output partitions defined by the partition names

    Args:
        partitions (Sequence[str]): the names of the partitions
        data_frames (Sequence[pd.DataFrame]): the dataframes that make up each partition

    Returns:
        Dict[str, pd.DataFrame]: a dictionary appropriate for handing off to kedro to write to disk

    Notes:
    ------
    The names of the partitions need to be appropriate.  In other words, if the `filename_suffix` is specified in the config, then the :param partitions: names shouldn't have an extension
    """
    partitions = {}
    DEBUG(f"create_partitions: {len(data_frames)=} {type(data_frames)=}")
    if len(data_frames) == 1:
        partitions = {str(partition_keys): data_frames}
    else:
        partitions = {str(p): d for p, d in zip(partition_keys, data_frames)}
    return partitions


def combine_data_vertically(*dataframes: Sequence[pd.DataFrame]) -> pd.DataFrame:
    """
    Combine any sequence of datasets
    the reason I'm using *datasets is that they will likely be passed in as *args
    rather than truly a list of datasets
    """
    if len(dataframes) == 1:
        return dataframes[0]

    combined_dataframes = pd.DataFrame()
    for d in dataframes:
        combined_dataframes = pd.concat([combined_dataframes, d])

    return combined_dataframes


def load_partitions(
    partitioned_input: Dict[str, Callable[[], Any]]
) -> Sequence[pd.DataFrame]:
    """
    Load up all the different data partitions into a single list of dataframes
    """
    data = []
    for _, partition_load_func in sorted(partitioned_input.items()):
        partition_data = partition_load_func()  # load the actual partition data
        data.append(partition_data)
    return data


def combine_data_horizontal(*dataframes: Sequence[pd.DataFrame]) -> pd.DataFrame:
    """
    Put together multiple datasets, adding in the unique columns

    Returns:
        pd.DataFrame: [description]
    """
    joined_dataframes = pd.concat(dataframes, axis=1)
    duplicated_columns = joined_dataframes.columns.duplicated(keep="first")
    combined_dataframes = joined_dataframes.loc[:, ~duplicated_columns]
    return combined_dataframes


def concat_partitions(partitioned_input: Dict[str, Callable[[], Any]]) -> pd.DataFrame:
    """Concatenate input partitions into one pandas DataFrame.

    Parameters
    ----------
        partitioned_input - dict(str, function)
            A dictionary with partition ids as keys and load functions as values.
        nfl_year: int, None
            If specified, the year will be populated with this value and the partition key will be assumed to be the week
            If not specified (None), it will be assumed that the partition key is actually the year

    Returns
    -------
        Pandas DataFrame representing a concatenation of all loaded partitions.
    """
    result = pd.DataFrame()

    for partition_key, partition_load_func in sorted(partitioned_input.items()):
        partition_data = partition_load_func()  # load the actual partition data
        # BUG: Assuming that the partition key is on year, though we know this may not be the case:
        partition_data[Stats.YEAR] = partition_key
        partition_data[Stats.NFL_WEEK] = NFL_SEASON
        # concat with existing result
        result = pd.concat([result, partition_data], ignore_index=True, sort=True)
    return result


def pass_thru(input_df: pd.DataFrame) -> pd.DataFrame:
    return input_df


def drop_unknown_columns(input_df: pd.DataFrame) -> pd.DataFrame:
    return input_df.drop(
        columns=[c for c in input_df.columns if "Unnamed:" in c], errors="ignore"
    )


def noop(*data_frames: pd.DataFrame) -> Sequence[pd.DataFrame]:
    return list(data_frames)
