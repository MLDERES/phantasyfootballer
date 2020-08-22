from pandas.core.dtypes.inference import is_list_like
from typing import Union, Any, List, Sequence
import pandas as pd


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
                f"Value of item was {item} expected either " f"a single value or list-like"
            )
    elif is_list_like(item):
        retVal = list(item)
    else:
        retVal = [item]
    return retVal


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

    ALL_STATS = [
        PASS_ATT,
        PASS_COMP,
        PASS_YDS,
        PASS_TDS,
        PASS_INT,
        RUSH_ATT,
        RUSH_YDS,
        RUSH_TDS,
        RCV_TGT,
        RCV_REC,
        RCV_YDS,
        RCV_TDS,
        DST_SACK,
        DST_INT,
        DST_FUM_REC,
        DST_FUM_FF,
        DST_TD,
        DST_SAFE,
        DST_PA,
        MISC_FL,
        RANK,
        POS_RANK,
        FANTASY_POINTS,
        PCT_TYPICAL_POS,
        PCT_MEAN_POS,
        PCT_MEDIAN_POS,
        PCT_TYPICAL_OVR,
        PCT_MEAN_OVR,
        PCT_MEDIAN_OVR,
    ]

    VALUE_STATS = [
        POS_RANK,
        FANTASY_POINTS,
        PCT_TYPICAL_POS,
        PCT_MEAN_POS,
        PCT_MEDIAN_POS,
        PCT_TYPICAL_OVR,
        PCT_MEAN_OVR,
        PCT_MEDIAN_OVR,
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
