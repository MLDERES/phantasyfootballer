import pandas as pd


PRO_FOOTBALL_URL = 'https://www.pro-football-reference.com/'

def _make_path(year, stat_group):
    return f'{PRO_FOOTBALL_URL}/years/{year}/{stat_group}.htm'
   

def fetch_pfr_data_by_year(start_year, stat_group, **read_args):
    uri = _make_path(start_year, stat_group)
    print(f'Attempt to retrieve data from {uri}')
    return pd.read_html(uri, **read_args)[0]

def fetch_passing_data(start_year):
    return fetch_pfr_data_by_year(start_year, 'passing', attrs={'id':'Passing Table'})

def fetch_rushing_data(start_year):
    return fetch_pfr_data_by_year(start_year, 'rushing', attrs={'id':'rushing'}, header=1)

def fetch_receiving_data(start_year):
    return fetch_pfr_data_by_year(start_year, 'receiving', attrs={'id':'receiving'})