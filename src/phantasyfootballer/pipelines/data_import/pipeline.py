import logging
from kedro.pipeline import Pipeline, node

import phantasyfootballer.data_providers.nfl_hist as nfl_hist
from phantasyfootballer.common_nodes import concat_partitions, pass_thru
from .nodes import (
    average_stats_by_player,
    consolidate_player_positions,
    fixup_player_names,
    preferred_column_order,
)


LOCAL_PROJECTIONS = ["projections.annual.fp-local", "projections.annual.cbs-local"]

logger = logging.getLogger("phantasyfootballer.data_import")
DEBUG = logger.debug
INFO = logger.info

# Pipelines here
# [] Annual Results
# [*] Annual Projections
# [] Weekly Results
# [] Weekly Projections

##
# Expert Consensus Rating Pipelines
##


def create_fpecr_pipeline(**kwargs):
    return Pipeline([node(pass_thru, "fp_ecr_raw", "fp_fpecr_local")])


##
# Projection pipelines
##


def create_fp_proj_pipeline(**kwargs):
    # TODO: Allow this accept weekly and annual projections
    return Pipeline(
        [
            node(
                fixup_player_names,
                "projections.annual.fp-remote",
                "projections.annual.fp-local",
            )
        ]
    )


def create_cbs_proj_pipeline(**kwargs):
    # TODO: Allow this accept weekly and annual projections
    return Pipeline(
        [
            node(
                fixup_player_names,
                "projections.annual.cbs-remote",
                "projections.annual.cbs-local",
            )
        ]
    )


def create_annual_projections_pipeline(**kwargs):
    """
    Combine together all the annual projection sources into a single annual projection
    This only works for the current year, which is assumed

    Returns:
        Pipeline: this pipeline gets all the annual projections from various sources and combines them into a single projection via average statistics
    """
    return Pipeline(
        [
            create_fp_proj_pipeline(),
            create_cbs_proj_pipeline(),
            node(
                func=average_stats_by_player,
                inputs=LOCAL_PROJECTIONS,
                outputs="projections.annual",
            ),
        ]
    )


#######
# Results Pipelines
#######
def create_weekly_results_pipeline(start_date=None, end_date=None, **kwargs):
    """
    Gather the weekly results from the local and remote into a single sourc

    Load unprocessed partitions concat together the partitions,
        this takes care of setting the year column in the data on load
    Process the data
        - set the data source
        - remove unwanted columns
        - remap the names on the columns we do want
    fixup the player_names
    Add into the exisiting annual.results file for downstream processing
    """
    return Pipeline(
        [
            node(
                concat_partitions,
                inputs="results.weekly.raw",
                outputs="combined_weekly_results",
            ),
            node(
                fixup_player_names,
                inputs="combined_weekly_results",
                outputs="combined_weekly_results_b",
            ),
            node(
                consolidate_player_positions,
                inputs="combined_weekly_results_b",
                outputs="combined_weekly_results_c",
            ),
            node(
                func=preferred_column_order,
                inputs="combined_weekly_results_c",
                outputs="results.weekly",
            )
            # node(
            #     split_year_from_week,
            #     inputs="combined_weekly_results_b",
            #     outputs="results.weekly",
            # ),
        ]
    )


def create_annual_results_pipeline(**kwargs):
    """
    Pull together the annual results sources
    """
    return Pipeline(
        [
            node(concat_partitions, "results.season.raw", "results_raw"),
            node(nfl_hist.process_data, "results_raw", "combined_annual_results"),
            node(
                consolidate_player_positions,
                inputs="combined_annual_results",
                outputs="combined_annual_results_b",
            ),
            node(fixup_player_names, "combined_annual_results_b", "results.season"),
        ]
    )
