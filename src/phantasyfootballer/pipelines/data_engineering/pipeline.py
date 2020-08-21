from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    calculate_projected_points,
    calculate_position_rank,
    average_stats_by_player,
    percent_mean,
    percent_typical,
    combine_data_horizontal,
)


LOCAL_PROJECTIONS = ["fp_projections_local", "cbs_projections_local"]


average_stats_pipeline = Pipeline(
    [
        node(
            func=average_stats_by_player,
            inputs=LOCAL_PROJECTIONS,
            outputs="average_stats_by_player_data",
        ),
    ]
)
"""
TODO: This pipeline needs to do the following

Using the projections, 
    Figure the score, using the scheme supplied in the parameters
    Then rank the players by that scoring scheme
        Figure the value of that player using the mean player in that position
        Figure the value of the player using the 100th man algorithm
"""
score_ppr_pipeline = Pipeline(
    [node(calculate_projected_points("full_ppr"), "average_stats_by_player_data", "scored_ppr_data")]
)
score_half_ppr_pipeline = Pipeline(
    [
        node(
            calculate_projected_points("half_ppr"),
            "average_stats_by_player_data",
            "scored_half_ppr_data",
        )
    ]
)
score_std_pipeline = Pipeline(
    [
        node(
            calculate_projected_points("standard"),
            "average_stats_by_player_data",
            "scored_standard_data",
        )
    ]
)
percentile_pipeline = Pipeline(
    [
        node(percent_mean, "scored_data", "percent_mean_data", name="percent_mean_node",),
        node(
            # Calculate the rank by the 100th man
            percent_typical,
            "scored_data",
            "percent_typical_data",
            name="percent_typical_node",
        ),
        node(
            combine_data_horizontal,
            ["percent_mean_data", "percent_typical_data"],
            "final_score_data",
            name="final_scoring_node",
        ),
    ]
)

full_ppr_pipeline = pipeline(
    percentile_pipeline,
    inputs={"scored_data": "scored_ppr_data"},
    outputs={"final_score_data": "scoring.ppr"},
    namespace="ppr",
)

full_half_ppr_pipeline = pipeline(
    percentile_pipeline,
    inputs={"scored_data": "scored_half_ppr_data"},
    outputs={"final_score_data": "scoring.half_ppr"},
    namespace="hppr",
)

full_standard_pipeline = pipeline(
    percentile_pipeline,
    inputs={"scored_data": "scored_standard_data"},
    outputs={"final_score_data": "scoring.standard"},
    namespace="std",
)


final_scoring_ranking_pipeline = (
    score_ppr_pipeline
    + score_half_ppr_pipeline
    + score_std_pipeline
    + full_ppr_pipeline
    + full_half_ppr_pipeline
    + full_standard_pipeline
)


def create_pipeline():
    return Pipeline([average_stats_pipeline, final_scoring_ranking_pipeline])


# def create_pipeline(**kwargs):
#     return Pipeline(
#         [
#             # node ( func = combine_data_vertically,
#             #       inputs = PROJECTIONS,
#             #       outputs='combined_projection'
#             #       ),
#             node(func=average_stats_by_player, inputs=LOCAL_PROJECTIONS, outputs="average_stats_by_player",),
#             node(
#                 func=calculate_projected_points(scoring="full_ppr"),
#                 inputs="average_stats_by_player",
#                 outputs="scoring_model",
#             ),
#             node(func=calculate_position_rank(scoring="all"), inputs="scoring_model", outputs="projections",),
#         ]
#     )
