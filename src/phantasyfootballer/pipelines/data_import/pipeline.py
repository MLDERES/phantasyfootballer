from kedro.pipeline import Pipeline, node
from .nodes import pass_thru



def create_fpecr_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                pass_thru,
                "fp_fpecr_csv_raw",
                'fp_fpecr_local'
            )
        ]
    )

def create_fp_proj_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                pass_thru,
                "fp_projections_remote",
                'fp_projections_local'
            )
        ]
    )