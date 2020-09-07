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
    data_import_pipeline = di.create_pipeline()
    data_engineering_pipeline = de.create_pipeline()
    annual_results_import_pipeline = di.create_annual_results_pipeline()
    annual_projections_import_pipeline = di.create_annual_projections_pipeline()
    # data_science_pipeline = ds.create_pipeline()
    # ds_pipeline = ds.create_pipeline()

    return {
        "data_import": data_import_pipeline,
        "results.annual": annual_results_import_pipeline,
        "projections.annual": annual_projections_import_pipeline,
        "de": data_engineering_pipeline,
        "di": data_import_pipeline,
        "__default__": Pipeline([data_import_pipeline + data_engineering_pipeline]),
    }


# def create_pipelines(**kwargs) -> Dict[str, Pipeline]:
#     """Create the project's pipeline.

#     Args:
#         kwargs: Ignore any additional arguments added in the future.

#     Returns:
#         A mapping from a pipeline name to a ``Pipeline`` object.

#     """
#     # data_engineering_pipeline = de.create_pipeline()
#     # # data_science_pipeline = ds.create_pipeline()
#     # #fp_ecr_pipeline = di.create_fpecr_pipeline()
#     # annual_results_pipeline = di.create_annual_results_pipeline()
#     # weekly_results_pipeline = di.create_weekly_results_pipeline()
#     # weekly_projections_pipeline = di.create_weekly_projections_pipeline()
#     annual_projections_pipeline = di.create_annual_projections_pipeline()
#     # data_import_weekly_pipeline = weekly_projections_pipeline + weekly_results_pipeline
#     # data_import_annual_pipeline = annual_projections_pipeline + annual_results_pipeline

#     return {
#         # "de": data_engineering_pipeline,
#         # "di_weekly": data_import_weekly_pipeline,
#         # "di_annual": data_import_annual_pipeline,
#         # 'annual_results': annual_results_pipeline,
#         # 'weekly_results': weekly_results_pipeline,
#         # 'annual_projections': annual_projections_pipeline,
#         # 'weekly_projections': weekly_projections_pipeline,
#         # "__default__": data_import_weekly_pipeline + data_engineering_pipeline,
#         "annual_projections":annual_projections_pipeline,
#         "_default__": annual_projections_pipeline
#     }
