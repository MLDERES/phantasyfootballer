import pytest

from kedro.framework.context import load_context

from phantasyfootballer.common import Stats
from phantasyfootballer.pipelines.data_engineering.nodes import (
    _craft_scoring_dict,
    _fetch_scoring_schemes,
)
from phantasyfootballer.settings import BASE_DIR


@pytest.fixture
def catalog():
    proj_path = BASE_DIR
    context = load_context(proj_path)
    catalog = context.catalog
    return catalog


def test_craft_scoring_scheme(self):
    ppr_dict = _craft_scoring_dict("full_ppr")
    assert ppr_dict[Stats.RCV_REC] == 1


def test_fetch_scoring_schemes(self):
    result = _fetch_scoring_schemes()
    assert "standard" in result
