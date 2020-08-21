from typing import Any, Dict, Union, List, Sequence
from phantasyfootballer.settings import *
from phantasyfootballer.common import Stats, get_list
import pandas as pd
from kedro.config import ConfigLoader
from functools import reduce, partial, update_wrapper

String_or_List = Union[str, List[str]]

def _craft_scoring_dict(scheme: str) -> Dict[str, Any]:
    """
    Look up the scoring system in the scoring.yml file 
    """
    conf_paths = ["conf/base", "conf/local"]
    conf_loader = ConfigLoader(conf_paths)
    conf_scoring = conf_loader.get("scoring*")
    return conf_scoring[scheme]

    # def_scoring = conf_scoring['standard']
    # scheme_scoring = conf_scoring.get(scheme,{})
    # def_scoring.update(scheme_scoring)
    # return def_scoring


def _fetch_scoring_schemes() -> List[str]:
    conf_paths = ["conf/base", "conf/local"]
    conf_loader = ConfigLoader(conf_paths)
    conf_scoring = conf_loader.get("scoring*")
    return list(conf_scoring.keys())


def _calculate_projected_points(scoring: String_or_List, data: pd.DataFrame) -> pd.DataFrame:
    if scoring == "all":
        scoring_types = _fetch_scoring_schemes()
    else:
        scoring_types = get_list(scoring)
    for scoring_scheme in scoring_types:
        score_map = _craft_scoring_dict(scoring_scheme)
        df_pts = pd.DataFrame()
        for c in data.columns:
            if (m := score_map.get(c)) :
                df_pts[c + "_pts"] = data[c] * m
        data[Stats.FANTASY_POINTS] = round(df_pts.sum(axis=1), 2)

    return data


def calculate_projected_points(scoring: String_or_List) -> pd.DataFrame:
    return update_wrapper(partial(_calculate_projected_points, scoring), _calculate_projected_points)


def _calculate_position_rank(scoring: String_or_List, data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the rank by scoring method for all positions
    """
    if scoring == "all":
        scoring_types = _fetch_scoring_schemes()
    else:
        scoring_types = get_list(scoring)

    for scoring_scheme in scoring_types:
        data[Stats.rank(scoring_scheme)] = data[Stats.points(scoring_scheme)].rank(na_option="bottom", ascending=False)

    return data


def calculate_position_rank(scoring: String_or_List) -> pd.DataFrame:
    """

    """
    return update_wrapper(partial(_calculate_position_rank, scoring), _calculate_position_rank)



def average_stats_by_player(*dataframes: Sequence[pd.DataFrame]) -> pd.DataFrame:
    """
    Given multiple dataframes, average the value of the stats provided into a new dataframe  
    """
    if len(dataframes) == 1:
        return dataframes[0]

    # Pull all the dataframes into a single one
    df_all = pd.concat(dataframes)
    # Get the mean keeping the columns that matter
    df_all = df_all.groupby([PLAYER_NAME, TEAM, POSITION]).mean().fillna(0)
    # Drop all the players where they have 0 projections
    df_all = df_all[df_all.sum(axis=1) > 0].reset_index()
    # Drop positions we don't care about 
    df_all = df_all.query('position in ["QB","RB","TE","WR","DST"]').reset_index(drop=True)
    return df_all

def calculate_player_rank(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate player ranking in a few different ways

    Args:
        data (pd.DataFrame): datafrme of player stats including project fantasy points

    Returns:
        pd.DataFrame: same dataframe with additional columns for player rank (overall) and by position
    """    
    # Calculate overall rank by points
    data[Stats.RANK] = data[Stats.FANTASY_POINTS].rank(na_option="bottom", ascending=False)
    # Calculate rank by position
    data[Stats.POS_RANK] = data.groupby(POSITION)[Stats.FANTASY_POINTS].rank(na_option="bottom", ascending=False)
    return data

def percent_mean(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the mean points for the player position, then determine how much more value this player has than 
    other players in the same position

    Args:
        data (pd.DataFrame): the dataframe that has the players and a single scoring scheme

    Returns:
        pd.DataFrame: updated with percentage
    """
    pos_data = data.groupby(POSITION)[Stats.FANTASY_POINTS].mean()
    joined = data.join(pos_data,on=POSITION,rsuffix='avg')
    data[Stats.PCT_MEAN_POS] = joined[Stats.FANTASY_POINTS]/joined['fpavg']
    data[Stats.PCT_MEAN_OVR] = data[Stats.FANTASY_POINTS]/(data[Stats.FANTASY_POINTS].mean())
    return data


def percent_median(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the points expected as a percentage of the median player in the position

    Args:
        data (pd.DataFrame): the dataframe that has the players and a single scoring scheme

    Returns:
        pd.DataFrame: updated dataframe with a column that has identified the value of a player 
        relative to the typical player in his position
    """
    pos_data = data.groupby(POSITION)[Stats.FANTASY_POINTS].median()
    joined = data.join(pos_data,on=POSITION,rsuffix='_med')
    data[Stats.PCT_MEDIAN_POS] = joined[Stats.FANTASY_POINTS]/joined['fp_med']
    data[Stats.PCT_MEDIAN_OVR] = data[Stats.FANTASY_POINTS]/(data[Stats.FANTASY_POINTS].median())
    return data

# TODO: Need to calculate typical player.  Issue #21
def percent_typical(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the points expected as a percentage of the median player in the position

    Args:
        data (pd.DataFrame): the dataframe that has the players and a single scoring scheme

    Returns:
        pd.DataFrame: updated dataframe with a column that has identified the value of a player 
        relative to the typical player in his position
    """
    data[Stats.PCT_TYPICAL_OVR] = 1
    data[Stats.PCT_TYPICAL_POS] = 1
    return data

    



