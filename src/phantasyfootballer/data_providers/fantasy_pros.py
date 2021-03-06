from urllib.parse import urljoin
import pandas as pd
import requests

from phantasyfootballer.common import Stats, map_data_columns
from phantasyfootballer.settings import (
    DATA_DIR,
    PLAYER_NAME,
    POSITION,
    QB,
    SOURCE,
    TEAM,
)

FP_URL = "https://www.fantasypros.com/nfl/projections/"

QB_COL_MAP = {
    "ATT": Stats.PASS_ATT,
    "CMP": Stats.PASS_COMP,
    "YDS": Stats.PASS_YDS,
    "TDS": Stats.PASS_TDS,
    "ATT.1": Stats.RUSH_ATT,
    "YDS.1": Stats.RUSH_YDS,
    "TDS.1": Stats.RUSH_TDS,
    "INTS": Stats.PASS_INT,
    "FL": Stats.MISC_FL,
    "REC": Stats.RCV_REC,
    "Player": PLAYER_NAME,
}
FLEX_COL_MAP = {
    "ATT": Stats.RUSH_ATT,
    "YDS": Stats.RUSH_YDS,
    "TDS": Stats.RUSH_TDS,
    "REC": Stats.RCV_REC,
    "YDS.1": Stats.RCV_YDS,
    "TDS.1": Stats.RCV_TDS,
    "INTS": Stats.PASS_INT,
    "FL": Stats.MISC_FL,
    "POS": POSITION,
    "Player": PLAYER_NAME,
}


def fetch_projections(**kwargs):
    week = kwargs.get("week", "draft")
    df_qb = _get_projections("qb", week=week)
    df_flex = _get_projections("flex", week=week)

    # Make sure the the columns are correct and consistent
    df_qb = map_data_columns(df_qb, QB_COL_MAP)
    df_qb[POSITION] = QB
    df_flex = map_data_columns(df_flex, FLEX_COL_MAP)
    df_flex = _fixup_position(df_flex)

    df_all = df_flex.append(df_qb, sort=True)
    df_all = _fixup_playername(df_all)

    # Let's not keep the fantasy points around, that will just cause confusion
    df_all[SOURCE] = "FantasyPros"
    return df_all


def _fixup_position(df):
    df[POSITION] = df[POSITION].str.extract(r"([A-z]*)")
    df[POSITION] = df[POSITION].str.upper()
    return df


def _fixup_playername(df):
    new_df = df[PLAYER_NAME].str.extract(r"(?P<PName>.*) (?P<team>[A-Z]{2,3}$)")
    df[[PLAYER_NAME, TEAM]] = new_df[["PName", TEAM]]
    return df


def _get_projections(position, week="draft"):
    """
    """
    url = urljoin(FP_URL, f"{position}.php")
    r = requests.get(url, params={"week": week})
    df = pd.read_html(r.text, header=[1])[0]

    # Let's not keep the fantasy points around, that will just cause confusion
    df.drop(columns=["FPTS"], errors="ignore", inplace=True)
    return df


if __name__ == "__main__":
    df = fetch_projections()
    df.to_csv(DATA_DIR / "fantasy_pros_projection.csv")
