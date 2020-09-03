from typing import Dict
import pandas as pd
from phantasyfootballer.common import PLAYER_NAME, get_config, MERGE_NAME
import string


def pass_thru(input_df: pd.DataFrame) -> pd.DataFrame:
    return input_df


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
    data[PLAYER_NAME] = data[PLAYER_NAME].apply(_replace_player_name)
    data[MERGE_NAME] = data[PLAYER_NAME].apply(_create_player_merge_name)
    return data
