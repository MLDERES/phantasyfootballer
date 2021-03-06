from pathlib import Path
import pandas as pd
import pytest

from phantasyfootballer.run import ProjectContext
from phantasyfootballer.settings import BASE_DIR, PLAYER_NAME

TEST_FOLDER = Path(__file__).cwd() / "src/tests"
TEST_DATA_FOLDER = TEST_FOLDER / "mock_data"


@pytest.fixture(scope="module")
def project_context():
    return ProjectContext(BASE_DIR)


@pytest.fixture(scope="module")
def annual_actual() -> pd.DataFrame:
    return pd.read_csv(TEST_DATA_FOLDER / "actual_annual.csv", index_col=PLAYER_NAME)


@pytest.fixture(scope="module")
def projections_annual() -> pd.DataFrame:
    return pd.read_csv(
        TEST_DATA_FOLDER / "projections_annual.csv", index_col=PLAYER_NAME
    )


@pytest.fixture(scope="module")
def projections_weekly() -> pd.DataFrame:
    return pd.read_csv(
        TEST_DATA_FOLDER / "projections_weekly.csv", index_col=PLAYER_NAME
    )


@pytest.fixture(scope="module")
def actual_weekly() -> pd.DataFrame:
    return pd.read_csv(TEST_DATA_FOLDER / "actual_weekly.csv", index_col=PLAYER_NAME)


if __name__ == "__main__":
    df = projections_weekly()
    pass
