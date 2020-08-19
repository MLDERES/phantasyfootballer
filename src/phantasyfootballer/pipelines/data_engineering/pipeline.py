from kedro.pipeline import Pipeline, node
from .nodes import (
    calculate_projected_points,
    calculate_position_rank,
    average_stats_by_player,
)


LOCAL_PROJECTIONS = ["fp_projections_local", "cbs_projections_local"]


def create_pipeline(**kwargs):
    return Pipeline(
        [
            # node ( func = combine_data_vertically,
            #       inputs = PROJECTIONS,
            #       outputs='combined_projection'
            #       ),
            node(
                func=average_stats_by_player,
                inputs=LOCAL_PROJECTIONS,
                outputs="average_stats_by_player",
            ),
            node(
                func=calculate_projected_points(scoring="all"),
                inputs="average_stats_by_player",
                outputs="scoring_model",
            ),
            node(
                func=calculate_position_rank(scoring="all"),
                inputs="scoring_model",
                outputs="projections",
            ),
        ]
    )
