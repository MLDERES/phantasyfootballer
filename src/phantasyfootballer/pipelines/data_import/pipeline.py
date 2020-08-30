from kedro.pipeline import Pipeline, node

from .nodes import fixup_player_names, pass_thru


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


def create_pipeline(**kwargs):
    """
    the main data_import pipeline
    """
    return Pipeline([create_fp_proj_pipeline(), create_cbs_proj_pipeline()])
