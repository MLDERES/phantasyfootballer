import pandas as pd


PRO_FOOTBALL_URL = 'https://www.pro-football-reference.com/'

def _make_path(year, stat_group):
    return f'{PRO_FOOTBALL_URL}/years/{year}/{stat_group}.htm'
   

def fetch_pfr_data_by_year(start_year, stat_group, xpath):
    uri = _make_path(start_year, stat_group)
    print(f'Attempt to retrieve data from {uri} on Xpath {xpath}')
    return pd.read_html(uri, xpath, index_col='Player')[0]

def fetch_passing_data(start_year):
    return fetch_pfr_data_by_year(start_year, 'passing', 'Passing Table')