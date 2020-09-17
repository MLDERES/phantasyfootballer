import pandas as pd

PRO_FOOTBALL_URL = "https://www.pro-football-reference.com/"


def _make_path(year, stat_group):
    return f"{PRO_FOOTBALL_URL}/years/{year}/{stat_group}.htm"


def fetch_pfr_data_by_year(start_year, stat_group, **read_args):
    uri = _make_path(start_year, stat_group)
    print(f"Attempt to retrieve data from {uri}")
    return pd.read_html(uri, **read_args)[0]


def fetch_passing_data(start_year):
    return fetch_pfr_data_by_year(start_year, "passing", attrs={"id": "Passing Table"})


def fetch_rushing_data(start_year):
    return fetch_pfr_data_by_year(
        start_year, "rushing", attrs={"id": "rushing"}, header=1
    )


def fetch_receiving_data(start_year):
    return fetch_pfr_data_by_year(start_year, "receiving", attrs={"id": "receiving"})


def fetch_weekly_results(start_date: None, end_date: None):
    df = pd.read_html(
        "https://www.pro-football-reference.com/play-index/pgl_finder.cgi?request=1&match=game&year_min=2019&year_max=2019&season_start=1&season_end=-1&age_min=0&age_max=99&game_type=A&league_id=&team_id=&opp_id=&game_num_min=0&game_num_max=99&week_num_min=1&week_num_max=1&game_day_of_week=&game_location=&game_result=&handedness=&is_active=&is_hof=&c1stat=pass_att&c1comp=gt&c1val=1&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&order_by=pass_rating&from_link=1"
    )
    df
