import pandas as pd
from phantasyfootballer.common import (
    PLAYER_NAME,
    POSITION,
    SOURCE,
    TEAM,
    Stats,
    map_data_columns,
)


ALL_COL_MAP = {
    "Player": PLAYER_NAME,
    "Tm": TEAM,
    "Pos": POSITION,
    "Age": Stats.AGE,
    "G": Stats.GAMES,
    "GS": Stats.GAMES_STARTED,
    "Cmp": Stats.PASS_COMP,
    "PassingAtt": Stats.PASS_ATT,
    "PassingYds": Stats.PASS_YDS,
    "PassingTD": Stats.PASS_TDS,
    "Int": Stats.PASS_INT,
    "RushingYds": Stats.RUSH_YDS,
    "RushingTD": Stats.RUSH_TDS,
    "RushingAtt": Stats.RUSH_ATT,
    "Tgt": Stats.RCV_TGT,
    "Rec": Stats.RCV_REC,
    "ReceivingYds": Stats.RCV_YDS,
    "ReceivingTD": Stats.RCV_TDS,
    "FumblesLost": Stats.MISC_FL,
}


def process_data(data: pd.DataFrame) -> pd.DataFrame:
    ret_data = map_data_columns(data, ALL_COL_MAP)
    ret_data[SOURCE] = "nfl_hist"
    return ret_data
