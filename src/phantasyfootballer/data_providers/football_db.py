# Data from The Football Database
import logging
import re
from datetime import date
import furl
import pandas as pd

from phantasyfootballer.common import map_data_columns
from phantasyfootballer.settings import (
    AWAY_TEAM,
    DATA_DIR,
    HOME_TEAM,
    PLAYER_NAME,
    POSITION,
    SOURCE,
    Stats,
)

BASE_URL = "https://www.footballdb.com/fantasy-football/index.html"
DATA_SOURCE = "football_db"

CURRENT_YEAR = date.year

logger = logging.getLogger("phantasyfootballer")
DEBUG = logger.debug
INFO = logger.info

QB_COL_MAP = FLEX_COL_MAP = {
    "Player": PLAYER_NAME,
    "Att": Stats.PASS_ATT,
    "Cmp": Stats.PASS_COMP,
    "Yds": Stats.PASS_YDS,
    "TD": Stats.PASS_TDS,
    "Int": Stats.PASS_INT,
    "2pt": Stats.PT2_CONV_PASS,
    "Att.1": Stats.RUSH_ATT,
    "Yds.1": Stats.RUSH_YDS,
    "TD.1": Stats.RUSH_TDS,
    "2Pt.1": Stats.PT2_CONV_RUSH,
    "Rec": Stats.RCV_REC,
    "Yds.2": Stats.RCV_YDS,
    "TD.2": Stats.RCV_TDS,
    "2Pt.2": Stats.PT2_CONV_RCV,
    "FL": Stats.MISC_FL,
}


def get_stats(year: int = CURRENT_YEAR, week: int = 0) -> pd.DataFrame:
    week = "all" if week == 0 else week
    # Case matters for some reason with this provider
    df_qb = get_stats_for_position("QB", year, week)
    df_rb = get_stats_for_position("RB", year, week)
    df_wr = get_stats_for_position("WR", year, week)
    df_te = get_stats_for_position("TE", year, week)
    df_all = pd.concat([df_rb, df_wr, df_te, df_qb])

    # Make sure the the columns are correct and consistent
    df_all = map_data_columns(df_all, FLEX_COL_MAP)
    # Set the source, game and year
    df_all[SOURCE] = DATA_SOURCE
    df_all[Stats.NFL_WEEK] = week
    df_all[Stats.YEAR] = year

    # Grab the team and the opponent if possible
    if "Game" in df_all.columns:
        df[[AWAY_TEAM, HOME_TEAM]] = df.Game.str.split("@", expand=True)

    return df_all


def get_stats_for_position(position: str, year: int, week: int) -> pd.DataFrame:
    params = {"pos": position, "yr": year, "wk": week}
    f = furl.furl(BASE_URL)
    f.args = params
    DEBUG(f"Getting info for {position=} {year=} {week=} {f.url=}")
    df = pd.read_html(
        f.url,
        header=1,
        converters={"Player": lambda x: re.match(r".*(?=[A-Z]\.)", x)[0]},
    )[0]
    df[POSITION] = position
    return df


if __name__ == "__main__":
    df = get_stats(year=2020, week=0)
    df.to_csv(DATA_DIR / "fbdb.csv")
