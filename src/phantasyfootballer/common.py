from pandas.core.dtypes.inference import is_list_like
from typing import Union, Any, List


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

class Stats():

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
    ]

    @staticmethod
    def points(scheme : str) -> str:
        '''
        Create a column name representing points for a given scheme
        '''
        return f'pts_{scheme}'
    
    @staticmethod
    def rank(scheme: str) -> str:
        '''
        Create a column name representing rank for a given points scheme
        '''
        return f'rank_{scheme}'
        