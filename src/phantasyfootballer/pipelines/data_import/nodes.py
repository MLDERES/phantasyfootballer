import logging
import string
from typing import Dict
import pandas as pd
from phantasyfootballer.common import get_config, reorder_columns
from phantasyfootballer.settings import (
    MERGE_NAME,
    PLAYER_NAME,
    POSITION,
    TEAM,
    Stats,
)

logger = logging.getLogger("phantasyfootballer.data_import")
DEBUG = logger.debug
INFO = logger.info
WARN = logger.warn
ERROR = logger.error


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
    suffixes_to_remove = [" Jr.", " III", " ", " II", " Sr."]
    name = _player_names.get(name, name)
    for _ in suffixes_to_remove:
        if name.endswith(_):
            name = name[: -len(_)]
    return name


def _create_player_merge_name(name: str) -> str:
    """
    Create a common name for merging on
    """
    return "".join([_ for _ in name.lower() if _ in string.ascii_lowercase])


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


def consolidate_player_positions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Some of the older data gives players two positions or combination positions,
    for consistency, we want to ensure that players are only QB, RB, TE, WR, DST

    Args:
        df (pd.DataFrame): The dataset with the players in their raw positions

    Returns:
        pd.DataFrame: Our standardized positions
    """
    position_map = {
        "QB/P": "QB",
        "FB": "RB",
        "WR/K": "WR",
        "HB": "RB",
        "FL": "WR",
        "SE": "WR",
        "FL": "WR",
        "ZR": "WR",
        "XR": "WR",
        "RB/K": "RB",
        "WR/T": "WR",
        "Z": "WR",
        "KR/W": "WR",
        "RB/F": "WR",
        "X": "WR",
        "WR/R": "WR",
        "RB-K": "RB",
        "WR-K": "WR",
        "PR/W": "WR",
        "HB-K": "RB",
        "XWR": "WR",
        "FB/T": "RB",
        "TE-L": "TE",
        "WR-P": "WR",
        "TE/F": "TE",
        "TE/L": "TE",
        "XTE": "TE",
        "P-QB": "QB",
        "FB-R": "FB",
        "FB/R": "RB",
        "QB/W": "WR",
        "WR/P": "WR",
        "HB/K": "RB",
        "CB/W": "WR",
        "X-WR": "WR",
        "WR/D": "WR",
        "TR": "TE",
        "QB3": "QB",
        "RB/KR": "RB",
        "H-B": "RB",
        "RB-KR": "RB",
        "WR-KR": "WR",
        "QB-WR": "WR",
        "TE/LS": "TE",
        "3QB": "QB",
        "QB/WR": "WR",
        "#3 QB": "QB",
        "TB": "TE",
        "TE/W": "TE",
        "LWR": "WR",
        "RWR": "WR",
        "RB-F": "RB",
        "FB-T": "TE",
        "FB": "RB",
        "HB/F": "RB",
        "WR W": "WR",
        "WR-R": "WR",
        "QB-W": "WR",
        "KR-R": "RB",
        "TE-F": "TE",
        "0": "WR",
        "WC": "WR",
        "WR/RS": "WR",
        "WR/PR": "WR",
        "FB/DL": "RB",
        "FB/TE": "TE",
        "FB/RB": "RB",
    }
    df[POSITION] = df[POSITION].replace(to_replace=position_map, value=None)
    df = df.query('position in ["QB","RB","TE","WR","DST"]')
    return df


def preferred_column_order(df: pd.DataFrame) -> pd.DataFrame:
    df_r = reorder_columns(df, [Stats.NFL_YEAR, Stats.NFL_WEEK, PLAYER_NAME])
    return df_r
