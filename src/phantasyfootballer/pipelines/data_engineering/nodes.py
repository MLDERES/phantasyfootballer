from typing import Any, Dict, Union, List, Sequence
from phantasyfootballer.settings import *
from phantasyfootballer.common import Stats, get_list
import pandas as pd
from kedro.config import ConfigLoader
from functools import reduce, partial, update_wrapper


String_or_List = Union[str, List[str]]


def normalize_data_source(data: pd.DataFrame, stat_name: str, common_stats: Dict[str, any]) -> pd.DataFrame:
    """
    This node will take a data source that is provided and adjust the stats so that they have 
    a common stat column name.  Additionally, if there is a stat that is common to the entire dataset
    (e.g. NFL week, NFL year, all qbs) that isn't already part of the file then this will be set as well.

    Say for instance, that the provider returns a file called 2019_passing_stats.  The column NFL Year is
    not likley included, so you can have it included by specifying that in the common_stats dictionary.

    The mapping from a provider column name and the common name are taking from conf/project/parameters.yml
    """
    pass


def establish_position_rank(data):
    """
    This node will create a position rank based on projections
    """
    pass


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
        data[Stats.points(scoring_scheme)] = round(df_pts.sum(axis=1), 2)

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


def average_stats_by_player(*dataframes: Sequence[pd.DataFrame]) -> pd.DataFrame:
    """
    Given multiple dataframes, average the value of the stats provided into a new dataframe  
    """
    if len(dataframes) == 1:
        return dataframes[0]

    # Pull all the dataframes into a single one
    df_all = pd.concat(dataframes)
    # Get the mean keeping the columns that matter
    df_all = df_all.groupby(["player", "team", "position"]).mean().fillna(0)
    # Drop all the players where they have 0 projections
    df_all = df_all[df_all.sum(axis=1) > 0].reset_index()
    return df_all


def percent_mean(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the overall rank and position rank using the score provided

    Args:
        data (pd.DataFrame): the dataframe that has the players and a single scoring scheme

    Returns:
        pd.DataFrame: updated dataframe with two new columns, rank and position rank
    """
    return data


def percent_typical(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the points expected as a percentage of the median player in the position

    Args:
        data (pd.DataFrame): the dataframe that has the players and a single scoring scheme

    Returns:
        pd.DataFrame: updated dataframe with a column that has identified the value of a player 
        relative to the typical player in his position
    """
    return data


def combine_data_horizontal(*dataframes: Sequence[pd.DataFrame]) -> pd.DataFrame:
    return pd.concat(dataframes,axis=1)
    



