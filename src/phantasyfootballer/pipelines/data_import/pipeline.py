from kedro.pipeline import Pipeline, node

from .nodes import fixup_player_names, pass_thru, average_stats_by_player
import phantasyfootballer.common as common
import phantasyfootballer.data_providers.nfl_hist as nfl_hist

LOCAL_PROJECTIONS = ["projections.annual.fp-local", "projections.annual.cbs-local"]


def create_fpecr_pipeline(**kwargs):
    return Pipeline([node(pass_thru, "fp_ecr_raw", "fp_fpecr_local")])


def create_fp_proj_pipeline(**kwargs):
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
    return Pipeline(
        [create_fp_proj_pipeline(), create_cbs_proj_pipeline(), average_stats_pipeline]
    )


def create_annual_results_pipeline(**kwargs):
    return Pipeline(
        [
            node(common.concat_partitions, "results.annual.source", "results_raw"),
            node(nfl_hist.process_data, "results_raw", "results_fixed"),
            node(fixup_player_names, "results_fixed", "results.annual.raw"),
        ]
    )


def create_pipeline(**kwargs):
    """
    the main data_import pipeline
    """
    return Pipeline(
        [create_annual_results_pipeline(), create_annual_projections_pipeline()]
    )


average_stats_pipeline = Pipeline(
    [
        node(
            func=average_stats_by_player,
            inputs=LOCAL_PROJECTIONS,
            outputs="projections.annual",
        ),
    ]
)
