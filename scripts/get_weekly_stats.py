# This script will gather weekly stats, primarily used for in-season efforts

from tqdm import tqdm
import pandas as pd
from pathlib import Path
from phantasyfootballer.data_providers import nfl_hist
from phantasyfootballer.pipelines.data_import.nodes import fixup_player_names


def move_historical_data_to_raw():
    """
    """
    # Find all the files in the weekly folder, by year/week
    # Fix the columns
    # Write the file to the 01_raw/results.weekly folder
    DATA_DIR = Path("/workspaces/phantasyfootballer/data")
    print(f"{DATA_DIR=}")
    for f in tqdm(DATA_DIR.glob("00_external/weekly/*/*.csv")):
        year = f.parent.stem
        filename = f.name
        df = pd.read_csv(f)
        df = df.pipe(nfl_hist.process_data).pipe(fixup_player_names)
        new_path = DATA_DIR / "01_raw/results.weekly" / year
        new_path.mkdir(parents=True, exist_ok=True)
        df.to_csv(new_path / filename)


if __name__ == "__main__":
    move_historical_data_to_raw()
    # current_nfl_date = NFLDate(date.today())
    # current_week = current_nfl_date.week
    # current_year = current_nfl_date.year

    # df = get_stats(current_year, current_week)
    # df
