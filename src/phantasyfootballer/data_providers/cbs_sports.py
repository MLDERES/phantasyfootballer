import logging
from urllib.parse import urljoin
import pandas as pd
import requests

from phantasyfootballer.common import map_data_columns
from phantasyfootballer.settings import (
    DATA_DIR,
    PLAYER_NAME,
    POSITION,
    SOURCE,
    TEAM,
    Stats,
)

BASE_URL = "https://www.cbssports.com/fantasy/football/stats/"

QB_COL_MAP = {
    "Player": PLAYER_NAME,
    "att  Pass Attempts": Stats.PASS_ATT,
    "cmp  Pass Completions": Stats.PASS_COMP,
    "yds  Passing Yards": Stats.PASS_YDS,
    "td  Touchdowns Passes": Stats.PASS_TDS,
    "int  Interceptions Thrown": Stats.PASS_INT,
    "att  Rushing Attempts": Stats.RUSH_ATT,
    "yds  Rushing Yards": Stats.RUSH_YDS,
    "td  Rushing Touchdowns": Stats.RUSH_TDS,
    "fl  Fumbles Lost": Stats.MISC_FL,
}
FLEX_COL_MAP = {
    "Player": PLAYER_NAME,
    "att  Rushing Attempts": Stats.RUSH_ATT,
    "yds  Rushing Yards": Stats.RUSH_YDS,
    "td  Rushing Touchdowns": Stats.RUSH_TDS,
    "tgt  Targets": Stats.RCV_TGT,
    "yds  Receiving Yards": Stats.RCV_YDS,
    "td  Receiving Touchdowns": Stats.RCV_TDS,
    "fl  Fumbles Lost": Stats.MISC_FL,
    "rec  Receptions": Stats.RCV_REC,
}


def fetch_projections(**kwargs):
    # Case matters for some reason with this provider
    year = kwargs["year"]
    df_qb = _get_projections("QB", year)
    df_rb = _get_projections("RB", year)
    df_wr = _get_projections("WR", year)
    df_te = _get_projections("TE", year)
    df_flex = pd.concat([df_rb, df_wr, df_te])

    # Make sure the the columns are correct and consistent
    df_qb = map_data_columns(df_qb, QB_COL_MAP)
    df_flex = map_data_columns(df_flex, FLEX_COL_MAP)

    df_all = df_flex.append(df_qb, sort=True)
    df_all = _fixup_playername(df_all)

    # Let's not keep the fantasy points around, that will just cause confusion
    df_all[SOURCE] = "cbs_sports"
    return df_all


def _fixup_playername(df):
    """
    this is a complete hack, but the way they have returned the name is a travesty
    C. McCaffery RB CAR Christian McCaffery RB CAR
    """
    df_names = pd.DataFrame()
    df_names = df[PLAYER_NAME].str.extract(
        r"(?P<stuff>.*?)(?P<pos>[A-Z]{1,2})\s*(?P<team>[A-Z]{2,3}$)"
    )
    df_names[["stuff_2", "name"]] = df_names.stuff.str.extract(
        r"(?P<stuff2>[A-Z]{2}\s*[A-Z]{2,3})\s*(?P<name>.*)"
    )
    df_names["name"] = df_names["name"].str.rstrip()
    df_names.drop(columns=["stuff", "stuff_2"], inplace=True)

    df[[PLAYER_NAME, TEAM, POSITION]] = df_names[["name", "team", "pos"]]
    return df


def _get_projections(position, year):
    """
    """
    log = logging.getLogger("kedro.pipeline")
    log.info(f"cbs get_projections for {position} {year}")
    url = urljoin(BASE_URL, f"{position}/{year}/season/projections/nonppr")
    log.info(f"{url}")

    r = requests.get(url)
    df = pd.read_html(r.text, header=1)[0]

    # Let's not keep the fantasy points around, that will just cause confusion
    df.drop(columns=["FPTS"], errors="ignore", inplace=True)
    return df


if __name__ == "__main__":
    df = fetch_projections(year=2020)
    df.to_csv(DATA_DIR / "cbs_sports.csv")
