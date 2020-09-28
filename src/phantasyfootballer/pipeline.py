"""Construction of the master pipeline.
"""

import logging
from typing import Dict

from kedro.pipeline import Pipeline

from phantasyfootballer.pipelines import data_engineering as de
from phantasyfootballer.pipelines import data_import as di

# from phantasyfootballer.pipelines import data_science as ds

log = logging.getLogger("phantasyfootballer")


def create_pipelines(**kwargs) -> Dict[str, Pipeline]:
    """Create the project's pipeline.

    Args:
        kwargs: Ignore any additional arguments added in the future.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.

    """
    data_engineering_pipeline = de.create_pipeline()
    annual_results_import_pipeline = di.create_annual_results_pipeline()
    weekly_results_import_pipeline = di.create_weekly_results_pipeline()

    annual_projections_import_pipeline = di.create_annual_projections_pipeline()
    # weekly_projections_import_pipeline = di.create_weekly_projections_pipeline()

    # data_science_pipeline = ds.create_pipeline()
    # ds_pipeline = ds.create_pipeline()

    return {
        "results.annual": annual_results_import_pipeline,
        "projections.annual": annual_projections_import_pipeline,
        "results.weekly": weekly_results_import_pipeline,
        # TODO: #41 weekly_projections_pipeline
        # #"projections.weekly": weekly_projections_import_pipeline,
        "de": data_engineering_pipeline,
        "__default__": Pipeline(
            [
                annual_results_import_pipeline
                + annual_projections_import_pipeline
                + data_engineering_pipeline
            ]
        ),
    }
