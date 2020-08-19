import requests
from urllib.parse import urljoin
import pandas as pd
from phantasyfootballer.settings import *

FP_URL = "https://www.fantasypros.com/nfl/projections/"

QB_COL_MAP = {
    "ATT": PASS_ATT,
    "CMP": PASS_COMP,
    "YDS": PASS_YDS,
    "TDS": PASS_TDS,
    "ATT.1": RUSH_ATT,
    "YDS.1": RUSH_YDS,
    "TDS.1": RUSH_TDS,
    "INTS": PASS_INT,
    "FL": MISC_FL,
    "REC": RCV_REC,
    "Player": PLAYER_NAME,
}
FLEX_COL_MAP = {
    "ATT": RUSH_ATT,
    "YDS": RUSH_YDS,
    "TDS": RUSH_TDS,
    "REC": RCV_REC,
    "YDS.1": RCV_YDS,
    "TDS.1": RCV_TDS,
    "POS": POSITION,
    "INTS": PASS_INT,
    "FL": MISC_FL,
    "REC": RCV_REC,
    "POS": POSITION,
    "Player": PLAYER_NAME,
}


def fetch_projections(week="draft"):
    df_qb = _get_projections("qb", week=week)
    df_flex = _get_projections("flex", week=week)

    # Make sure the the columns are correct and consistent
    df_qb.rename(columns=QB_COL_MAP, inplace=True)
    df_qb[POSITION] = "QB"
    df_flex.rename(columns=FLEX_COL_MAP, inplace=True)
    df_flex = _fixup_position(df_flex)

    df_all = df_flex.append(df_qb, sort=True)
    df_all = _fixup_playername(df_all)

    # Let's not keep the fantasy points around, that will just cause confusion
    df_all.drop(columns=["FPTS"], errors="ignore", inplace=True)
    df_all = _set_column_order(df_all)
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


def _set_column_order(df):
    return df.reindex(
        columns=[PLAYER_NAME, TEAM, POSITION, POS_RANK]
        + [PASS_ATT, PASS_COMP, PASS_INT, PASS_TDS, PASS_YDS]
        + [RCV_REC, RCV_TDS, RCV_YDS]
        + [RUSH_ATT, RUSH_YDS, RUSH_TDS]
        + [MISC_FL]
    )


if __name__ == "__main__":
    df = fetch_projections()
    df.to_csv(DATA_DIR / "fantasy_pros_projection.csv")
