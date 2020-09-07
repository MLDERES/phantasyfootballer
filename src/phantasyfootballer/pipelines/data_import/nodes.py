from typing import Dict, Sequence, Callable, Any
import pandas as pd
from phantasyfootballer.common import (
    PLAYER_NAME,
    get_config,
    MERGE_NAME,
    Stats,
    TEAM,
    POSITION,
    NFL_WEEK_ALL,
)
import string
import logging

logger = logging.getLogger("phantasyfootballer.data_import")
DEBUG = logger.debug
INFO = logger.info
WARN = logger.warn


def pass_thru(input_df: pd.DataFrame) -> pd.DataFrame:
    return input_df


def noop(*data_frames: pd.DataFrame) -> Sequence[pd.DataFrame]:
    return list(data_frames)


def _get_player_names() -> Dict[str, str]:
    params = get_config("param*")
    player_names = params["player_name_alias"]
    name_map = {}
    for k, v in player_names.items():
        for alt_name in v:
            name_map[alt_name] = k
    return name_map


_player_names = _get_player_names()


def _replace_player_name(name: str) -> str:
    return _player_names.get(name, name).rstrip(" Jr.").rstrip(" III").rstrip(" ")


def _create_player_merge_name(name: str) -> str:
    """
    Create a common name for merging on
    """
    return "".join([_ for _ in name.lower() if _ in string.ascii_lowercase])
    # return _player_names.get(name, name).rstrip(" Jr.").rstrip(" III").rstrip(" ")


def fixup_player_names(data: pd.DataFrame) -> pd.DataFrame:
    """
    Using the lookup dictionary in the `parameters.yml` file, make sure that names match
    in case of different spellings or suffixes.

    For instance,
        `Mitch Trubisky == Mitchell Trubisky`

    Parameters:
    -----------
    data : pd.DataFrame
        the dataset

    Returns:
    --------
    the updated dataset
    """
    DEBUG("fixup_player_names()")
    data[PLAYER_NAME] = data[PLAYER_NAME].apply(_replace_player_name)
    data[MERGE_NAME] = data[PLAYER_NAME].apply(_create_player_merge_name)
    return data


def split_year_from_week(data: pd.DataFrame) -> pd.DataFrame:
    """
    Because we have used the partition key as the NFL year, the year/week need to be put into the appropriate columns
    """
    data[[Stats.YEAR, Stats.NFL_WEEK]] = data[Stats.YEAR].str.split("/", expand=True)
    data[Stats.NFL_WEEK] = data[Stats.NFL_WEEK].apply(lambda x: int(x.lstrip("week")))
    return data


def average_stats_by_player(*dataframes: pd.DataFrame) -> pd.DataFrame:
    """
    Given multiple dataframes, average the value of the stats provided into a new dataframe
    """
    DEBUG("average_stat_by_player()")
    if len(dataframes) == 1:
        return dataframes[0]

    # Pull all the dataframes into a single one
    df_all = pd.concat(dataframes)
    # Get the mean keeping the columns that matter
    df_all = df_all.groupby([PLAYER_NAME, TEAM, POSITION]).mean().fillna(0)
    # Drop all the players where they have 0 projections
    df_all = df_all[df_all.sum(axis=1) > 0].reset_index()
    # Drop positions we don't care about
    df_all = df_all.query('position in ["QB","RB","TE","WR","DST"]').reset_index(
        drop=True
    )
    return df_all


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
        partition_data[Stats.NFL_WEEK] = NFL_WEEK_ALL
        # concat with existing result
        result = pd.concat([result, partition_data], ignore_index=True, sort=True)
    return result
