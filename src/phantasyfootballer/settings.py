from pathlib import Path
from enum import Enum

BASE_DIR = Path(__file__).parents[2]

RANKINGS = 'fp_rank'
PROJECTIONS = 'fp_projection'

class Stat(Enum):
    PLAYER_NAME = 'player'
    TEAM = 'team'
    POSITION = 'position'
    POS_RANK = 'pos_rank'
    PASS_ATT = 'pass_att'
    PASS_COMP = 'pass_comp'
    PASS_YDS = 'pass_yds'
    PASS_TDS = 'pass_tds'
    PASS_INT = 'pass_int'
    RUSH_ATT = 'rush_att'
    RUSH_YDS = 'rush_yds'
    RUSH_TDS = 'rush_tds'
    RCV_TGT = 'rcv_targets'
    RCV_REC = 'rcv_rec'
    RCV_YDS = 'rcv_yds'
    RCV_TDS = 'rcv_tds'
    DST_SACK = 'dst_sack'
    DST_INT = 'dst_int'
    DST_FUM_REC = 'dst_fc'
    DST_FUM_FF = 'dst_ff'
    DST_TD = 'dst_td'
    DST_SAFE = 'dst_sft'
    DST_PA = 'dst_pa'
    MISC_FL = 'fumble_lost'
    FP_STD = 'fp_std'
    FP_HALF = 'fp_hppr'
    FP_FULL = 'fp_ppr'

if __name__ == "__main__":
    print(BASE_DIR)