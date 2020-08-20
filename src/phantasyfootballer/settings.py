from pathlib import Path
from .common import Stats

BASE_DIR = Path(__file__).parents[2]
DATA_DIR = BASE_DIR / "data"

RANKINGS = "fp_rank"
PROJECTIONS = "fp_projection"

PLAYER_NAME = "player"
TEAM = "team"
POSITION = "position"
SOURCE = "source"

# Positions
QB = "QB"
TE = "TE"
RB = "RB"
WR = "WR"
K = "K"
DST = "DST"

KEEPER_COLUMNS = [
    PLAYER_NAME,
    TEAM,
    POSITION,
    Stats.PASS_ATT,
    Stats.PASS_COMP,
    Stats.PASS_INT,
    Stats.PASS_TDS,
    Stats.PASS_YDS,
    Stats.RCV_REC,
    Stats.RCV_TDS,
    Stats.RCV_YDS,
    Stats.RUSH_ATT,
    Stats.RUSH_YDS,
    Stats.RUSH_TDS,
    Stats.MISC_FL,
]

if __name__ == "__main__":
    print(BASE_DIR)
