from pathlib import Path

BASE_DIR = Path(__file__).parents[2]
DATA_DIR = BASE_DIR / "data"

RANKINGS = "fp_rank"
PROJECTIONS = "fp_projection"

PLAYER_NAME = "player"
TEAM = "team"
OPPONENT = "opp_team"
POSITION = "position"
SOURCE = "source"
MERGE_NAME = "pname_merge"
HOME_TEAM = "home"
AWAY_TEAM = "away"

# When this value is the NFL week, that means it's for the entire year
NFL_WEEK_ALL = 99

# Positions
QB = "QB"
TE = "TE"
RB = "RB"
WR = "WR"
K = "K"
DST = "DST"


class Stats:
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
    FANTASY_POINTS = "fp"
    RANK = "overall_rank"
    PCT_TYPICAL_POS = "percent_typical_position"
    PCT_MEAN_POS = "percent_average_position"
    PCT_MEDIAN_POS = "percent_median_position"
    PCT_TYPICAL_OVR = "percent_typical_overall"
    PCT_MEAN_OVR = "percent_average_overall"
    PCT_MEDIAN_OVR = "percent_median_overall"
    # Only the top players are used in the evaluation of value
    TOP_PLAYER = "is_top_player"
    POS_VALUE = "positional_value"
    POS_VALUE_REM = "pos_value_remaining"
    DIFF_POS_VALUE_REM = "pos_value_remaining_diff"
    # The percent of points that will be scored by all players in the league
    OVR_VALUE = "overall_value"
    # The percent points left after this player is taken
    OVR_VALUE_REM = "overall_value_left"
    YEAR = "year"  # for historical data
    NFL_WEEK = "nfl_week"  # a given nfl week
    AGE = "age"  # player age
    GAMES = "games"  # number of games played
    GAMES_STARTED = "gs"  # number of games a player started
    PT2_CONV_RUSH = "2pt_Rush"  # 2 point conversion rushing
    PT2_CONV_RCV = "2pt_Rec"  # 2 point conversion receiving
    PT2_CONV_PASS = "2pt_Pass"

    VALUE_STATS = [
        POS_RANK,
        FANTASY_POINTS,
        PCT_TYPICAL_POS,
        PCT_MEAN_POS,
        PCT_MEDIAN_POS,
        PCT_TYPICAL_OVR,
        PCT_MEAN_OVR,
        PCT_MEDIAN_OVR,
        POS_VALUE,
        POS_VALUE_REM,
    ]

    @staticmethod
    def points(scheme: str) -> str:
        """
        Create a column name representing points for a given scheme
        """
        return f"pts_{scheme}"

    @staticmethod
    def rank(scheme: str) -> str:
        """
        Create a column name representing rank for a given points scheme
        """
        return f"rank_{scheme}"


KEEPER_COLUMNS = [
    ## These are used by the providers to know which fields are required and which can be ignored
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
    Stats.YEAR,
    Stats.AGE,
    Stats.GAMES,
    Stats.GAMES_STARTED,
    Stats.YEAR,
    Stats.NFL_WEEK,
]
