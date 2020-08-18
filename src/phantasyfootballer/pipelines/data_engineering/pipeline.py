from kedro.pipeline import Pipeline, node
from .nodes import calculate_projected_points, calculate_position_rank

def create_pipeline(**kwargs):
    return Pipeline(
        [
           node (
               calculate_projected_points(scoring='all'),
               'fp_projections_local',
               'scoring_model'
           ),
           node (
               calculate_position_rank(scoring='all'),
               'scoring_model',
               'projections'
           ),
        ]
    )
