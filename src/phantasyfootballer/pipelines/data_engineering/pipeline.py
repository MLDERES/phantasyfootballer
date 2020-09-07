import phantasyfootballer.common as common
from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    calculate_player_rank,
    calculate_projected_points,
    filter_by_position,
    percent_mean,
    percent_median,
    percent_typical,
    remaining_positional_value,
)


"""
    This pipeline needs to do the following

    Using the projections,
    Figure the score, using the scheme supplied in the parameters
    Then rank the players by that scoring scheme
        Figure the value of that player using the mean player in that position
        Figure the value of the player using the 100th man algorithm
"""
score_ppr_pipeline = Pipeline(
    [
        node(
            calculate_projected_points("full_ppr"),
            "projections.annual",
            "scored_ppr_data",
        )
    ]
)
score_half_ppr_pipeline = Pipeline(
    [
        node(
            calculate_projected_points("half_ppr"),
            "projections.annual",
            "scored_half_ppr_data",
        )
    ]
)
score_std_pipeline = Pipeline(
    [
        node(
            calculate_projected_points("standard"),
            "projections.annual",
            "scored_standard_data",
        )
    ]
)
score_custom_pipeline = Pipeline(
    [
        node(
            calculate_projected_points("custom"),
            "projections.annual",
            "scored_custom_data",
        )
    ]
)
ranking_pipeline = Pipeline(
    [
        node(
            calculate_player_rank,
            "scored_data",
            "ranked_data",
            name="overall_rank_node",
        ),
        node(
            filter_by_position,
            ["ranked_data", "params:player_filter"],
            "filtered_player_data",
            name="filter_players",
        ),
        # For median and mean values, I want to be sure we are limiting to the players that are filtered
        node(
            percent_median,
            "filtered_player_data",
            "percent_median_data",
            name="percent_median_node",
        ),
        node(
            percent_mean,
            "filtered_player_data",
            "percent_mean_data",
            name="percent_mean_node",
        ),
        node(
            # Calculate the rank by the 100th man - no need to filter!
            percent_typical,
            "filtered_player_data",
            "percent_typical_data",
            name="percent_typical_node",
        ),
        node(
            remaining_positional_value,
            "filtered_player_data",
            "positional_val_data",
            name="remaining_val_node",
        ),
        node(
            common.combine_data_horizontal,
            [
                "percent_mean_data",
                "percent_typical_data",
                "percent_median_data",
                "positional_val_data",
            ],
            "final_score_data",
            name="final_scoring_node",
        ),
    ]
)
# Each of the following pipelines are here to do the ranking for each
#  scoring type
full_ppr_pipeline = pipeline(
    ranking_pipeline,
    inputs={"scored_data": "scored_ppr_data"},
    outputs={"final_score_data": "scoring.ppr"},
    namespace="ppr",
)

full_half_ppr_pipeline = pipeline(
    ranking_pipeline,
    inputs={"scored_data": "scored_half_ppr_data"},
    outputs={"final_score_data": "scoring.half_ppr"},
    namespace="hppr",
)

full_standard_pipeline = pipeline(
    ranking_pipeline,
    inputs={"scored_data": "scored_standard_data"},
    outputs={"final_score_data": "scoring.standard"},
    namespace="std",
)
full_custom_pipeline = pipeline(
    ranking_pipeline,
    inputs={"scored_data": "scored_custom_data"},
    outputs={"final_score_data": "scoring.custom"},
    namespace="custom",
)

final_scoring_ranking_pipeline = (
    score_ppr_pipeline
    + score_half_ppr_pipeline
    + score_std_pipeline
    + score_std_pipeline
    + full_ppr_pipeline
    + full_half_ppr_pipeline
    + full_standard_pipeline
    + full_standard_pipeline
)


def create_pipeline():
    return Pipeline([final_scoring_ranking_pipeline])
