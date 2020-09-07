from pathlib import Path
from typing import Any, Dict, List, Sequence, Union, Optional, Callable

import pandas as pd
from kedro.config import TemplatedConfigLoader
from pandas.core.dtypes.inference import is_list_like
import logging

logger = logging.getLogger("phantasyfootballer")
DEBUG = logger.debug
INFO = logger.info

BASE_DIR = Path(__file__).parents[2]
DATA_DIR = BASE_DIR / "data"

RANKINGS = "fp_rank"
PROJECTIONS = "fp_projection"

PLAYER_NAME = "player"
TEAM = "team"
POSITION = "position"
SOURCE = "source"
MERGE_NAME = "pname_merge"

# When this value is the NFL week, that means it's for the entire year
NFL_WEEK_ALL = 99

# Positions
QB = "QB"
TE = "TE"
RB = "RB"
WR = "WR"
K = "K"
DST = "DST"


class Stats:
    POS_RANK = "pos_rank"
    PASS_ATT = "pass_att"
    PASS_COMP = "pass_comp"
    PASS_YDS = "pass_yds"
    PASS_TDS = "pass_tds"
    PASS_INT = "pass_int"
    RUSH_ATT = "rush_att"
    RUSH_YDS = "rush_yds"
    RUSH_TDS = "rush_tds"
    RCV_TGT = "rcv_targets"
    RCV_REC = "rcv_rec"
    RCV_YDS = "rcv_yds"
    RCV_TDS = "rcv_tds"
    DST_SACK = "dst_sack"
    DST_INT = "dst_int"
    DST_FUM_REC = "dst_fumble_rec"
    DST_FUM_FF = "dst_force_fum"
    DST_TD = "dst_td"
    DST_SAFE = "dst_sft"
    DST_PA = "dst_pa"
    MISC_FL = "fumble_lost"
    FP_STD = "fp_std"
    FP_HALF = "fp_hppr"
    FP_FULL = "fp_ppr"
    FANTASY_POINTS = "fp"
    RANK = "overall_rank"
    PCT_TYPICAL_POS = "percent_typical_position"
    PCT_MEAN_POS = "percent_average_position"
    PCT_MEDIAN_POS = "percent_median_position"
    PCT_TYPICAL_OVR = "percent_typical_overall"
    PCT_MEAN_OVR = "percent_average_overall"
    PCT_MEDIAN_OVR = "percent_median_overall"
    # Only the top players are used in the evaluation of value
    TOP_PLAYER = "is_top_player"
    POS_VALUE = "positional_value"
    POS_VALUE_REM = "pos_value_remaining"
    DIFF_POS_VALUE_REM = "pos_value_remaining_diff"
    # The percent of points that will be scored by all players in the league
    OVR_VALUE = "overall_value"
    # The percent points left after this player is taken
    OVR_VALUE_REM = "overall_value_left"
    YEAR = "year"  # for historical data
    NFL_WEEK = "nfl_week"  # a given nfl week
    AGE = "age"  # player age
    GAMES = "games"  # number of games played
    GAMES_STARTED = "gs"  # number of games a player started

    VALUE_STATS = [
        POS_RANK,
        FANTASY_POINTS,
        PCT_TYPICAL_POS,
        PCT_MEAN_POS,
        PCT_MEDIAN_POS,
        PCT_TYPICAL_OVR,
        PCT_MEAN_OVR,
        PCT_MEDIAN_OVR,
        POS_VALUE,
        POS_VALUE_REM,
    ]

    @staticmethod
    def points(scheme: str) -> str:
        """
        Create a column name representing points for a given scheme
        """
        return f"pts_{scheme}"

    @staticmethod
    def rank(scheme: str) -> str:
        """
        Create a column name representing rank for a given points scheme
        """
        return f"rank_{scheme}"


KEEPER_COLUMNS = [
    ## These are used by the providers to know which fields are required and which can be ignored
    PLAYER_NAME,
    TEAM,
    POSITION,
    Stats.PASS_ATT,
    Stats.PASS_COMP,
    Stats.PASS_INT,
    Stats.PASS_TDS,
    Stats.PASS_YDS,
    Stats.RCV_REC,
    Stats.RCV_TDS,
    Stats.RCV_YDS,
    Stats.RUSH_ATT,
    Stats.RUSH_YDS,
    Stats.RUSH_TDS,
    Stats.MISC_FL,
    Stats.YEAR,
    Stats.AGE,
    Stats.GAMES,
    Stats.GAMES_STARTED,
    Stats.YEAR,
    Stats.NFL_WEEK,
]


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
        partition_data[Stats.NFL_WEEK] = NFL_WEEK_ALL
        # concat with existing result
        result = pd.concat([result, partition_data], ignore_index=True, sort=True)
    return result


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


def get_list(item: Union[Any, List[Any]], errors="ignore"):
    """
    Return a list from the item passed.
    If the item passed is a string, put it in a list.
    If the item is list like, then return it as a list.

    Parameters
    ----------
    item: str or list-like
        the thing or list to ensure is a list
    errors: {‘ignore’, ‘raise’, 'coerce}, default ‘ignore’
        If the item is None, then the return depends on the errors state
        If errors = 'raise' then raise an error if the list is empty
        If errors = 'ignore' then return None
        If errors = 'coerce' then return an empty list if possible

    Returns
    ------
    list
        the created list
    """
    retVal = None
    if item is None:
        if errors == "coerce":
            retVal = []
        elif errors == "raise":
            raise ValueError(
                f"Value of item was {item} expected either "
                f"a single value or list-like"
            )
    elif is_list_like(item):
        retVal = list(item)
    else:
        retVal = [item]
    return retVal


def get_config(
    file_glob: str, globals_dict: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    conf_paths = [str(BASE_DIR / "conf/base"), str(BASE_DIR / "conf/local")]
    config_loader = TemplatedConfigLoader(
        conf_paths, globals_pattern="*globals.yml", globals_dict=globals_dict
    )
    return config_loader.get(file_glob)


def map_data_columns(data: pd.DataFrame, column_map: Dict[str, str]) -> pd.DataFrame:
    """
    For raw stats in particular, rename the columns to be constant, and drop out the ones that we don't need not interested in

    Parameters:
    -----------
    data : pd.DataFrame
        the raw dataframe with the original column names
    column_map: Dict[str, str]
        a dictionary of the original column names and the new common name

    Returns:
    --------
    pd.DataFrame
        the modified dataframe with the columns renamed and the other field dropped
    """
    data.rename(columns=column_map, inplace=True)
    data = data.drop(columns=set(data.columns) - set(KEEPER_COLUMNS))
    return _reorder_columns(data, [PLAYER_NAME, TEAM, Stats.YEAR, Stats.NFL_WEEK])


def _reorder_columns(
    data: pd.DataFrame, fixed_columns: Union[str, Any]
) -> pd.DataFrame:
    columns_to_drop = data.columns.drop(fixed_columns, errors="ignore").tolist()
    new_col_order = (
        list(set(data.columns).intersection(fixed_columns)) + columns_to_drop
    )
    DEBUG(f"_reorder_columns {new_col_order=}")
    return data[new_col_order]


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
