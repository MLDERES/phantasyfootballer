import requests
from urllib.parse import urljoin
import pandas as pd
from phantasyfootballer.settings import *
import logging

BASE_URL = "https://www.cbssports.com/fantasy/football/stats/"

QB_COL_MAP = {
    "Player": PLAYER_NAME,
    "att  Pass Attempts": PASS_ATT,
    "cmp  Pass Completions": PASS_COMP,
    "yds  Passing Yards": PASS_YDS,
    "td  Touchdowns Passes": PASS_TDS,
    "int  Interceptions Thrown": PASS_INT,
    "att  Rushing Attempts": RUSH_ATT,
    "yds  Rushing Yards": RUSH_YDS,
    "td  Rushing Touchdowns": RUSH_TDS,
    "fl  Fumbles Lost": MISC_FL,
}
FLEX_COL_MAP = {
    "att  Rushing Attempts": RUSH_ATT,
    "yds  Rushing Yards": RUSH_YDS,
    "td  Rushing Touchdowns": RUSH_TDS,
    "tgt  Targets": RCV_TGT,
    "yds  Receiving Yards": RCV_YDS,
    "td  Receiving Touchdowns": RCV_TDS,
    "fl  Fumbles Lost": MISC_FL,
    "rec  Receptions": RCV_REC,
    "Player": PLAYER_NAME,
}


def fetch_projections(year):
    # Case matters for some reason with this provider
    df_qb = _get_projections("QB", year)
    df_rb = _get_projections("RB", year)
    df_wr = _get_projections("WR", year)
    df_te = _get_projections("TE", year)
    df_flex = pd.concat([df_rb, df_wr, df_te])

    # Make sure the the columns are correct and consistent
    df_qb.rename(columns=QB_COL_MAP, inplace=True)
    df_flex.rename(columns=FLEX_COL_MAP, inplace=True)

    df_all = df_flex.append(df_qb, sort=True)
    df_all = _fixup_playername(df_all)

    # Let's not keep the fantasy points around, that will just cause confusion
    df_all = df_all[
        [PLAYER_NAME, TEAM, POSITION,]
        + [PASS_ATT, PASS_COMP, PASS_INT, PASS_TDS, PASS_YDS]
        + [RCV_REC, RCV_TDS, RCV_YDS]
        + [RUSH_ATT, RUSH_YDS, RUSH_TDS]
        + [MISC_FL]
    ]
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
    df = fetch_projections(2020)
    df.to_csv(DATA_DIR / "cbs_sports.csv")
