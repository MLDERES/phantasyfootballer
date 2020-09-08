import logging
from typing import Any, Dict, List, Optional, Union
import pandas as pd
from pandas.core.dtypes.inference import is_list_like

from kedro.config import TemplatedConfigLoader

from .settings import BASE_DIR, KEEPER_COLUMNS, PLAYER_NAME, TEAM, Stats

logger = logging.getLogger("phantasyfootballer")
DEBUG = logger.debug
INFO = logger.info


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
    return reorder_columns(data, [PLAYER_NAME, TEAM, Stats.YEAR, Stats.NFL_WEEK])


def reorder_columns(data: pd.DataFrame, fixed_columns: Union[str, Any]) -> pd.DataFrame:
    """
    Change the order of columns for easier reading

    Parameters:
    ----------
    data : pd.DataFrame
        the dataframe to adjust
    fixed_columns:
        the column or columns that should be the first in the list
    """
    columns_to_drop = data.columns.drop(fixed_columns, errors="ignore").tolist()
    new_col_order = (
        list(set(data.columns).intersection(fixed_columns)) + columns_to_drop
    )
    DEBUG(f"reorder_columns {new_col_order=}")
    return data[new_col_order]


# def create_empty_pipline():
#     return Pipeline([node(noop, None, )])
