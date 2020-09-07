import phantasyfootballer.pipelines.data_import as di
from kedro.pipeline import Pipeline


def test_data_import_pipeline():
    pipeline = di.create_pipeline()
    assert isinstance(pipeline, Pipeline)
    assert any(pipeline.nodes)


def test_create_annual_projections_pipeline():
    pipeline = di.create_annual_projections_pipeline()
    assert isinstance(pipeline, Pipeline)
    assert any(pipeline.nodes)


def test_create_annual_results_pipeline():
    pipeline = di.create_annual_results_pipeline()
    assert isinstance(pipeline, Pipeline)
    assert any(pipeline.nodes)


if __name__ == "__main__":
    pass
