from kedro.pipeline import Pipeline, node

from .nodes import fixup_player_names, pass_thru
import phantasyfootballer.common as common
import phantasyfootballer.data_providers.nfl_hist as nfl_hist


def create_fpecr_pipeline(**kwargs):
    return Pipeline([node(pass_thru, "fp_ecr_raw", "fp_fpecr_local")])


def create_fp_proj_pipeline(**kwargs):
    return Pipeline(
        [node(fixup_player_names, "fp_projections_remote", "fp_projections_local")]
    )


def create_cbs_proj_pipeline(**kwargs):
    return Pipeline(
        [node(fixup_player_names, "cbs_projections_remote", "cbs_projections_local")]
    )


def create_historical_yearly_pipeline(**kwargs):
    return Pipeline(
        [
            node(common.concat_partitions, "historical_yearly_ext", "hist_raw"),
            node(nfl_hist.process_data, "hist_raw", "hist_fixed"),
            node(fixup_player_names, "hist_fixed", "historical_yearly_raw"),
        ]
    )


def create_pipeline(**kwargs):
    """
    the main data_import pipeline
    """
    return Pipeline(
        [
            create_historical_yearly_pipeline(),
            create_fp_proj_pipeline(),
            create_cbs_proj_pipeline(),
        ]
    )
