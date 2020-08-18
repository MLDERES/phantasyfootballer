from kedro.pipeline import Pipeline, node
from .nodes import calculate_projected_points

def create_pipeline(**kwargs):
    return Pipeline(
        [
           node (
               calculate_projected_points(scoring='standard'),
               'fp_projections_local',
               'standard_scoring_model'
           ),
           node (
               calculate_projected_points(scoring='full_ppr'),
               'standard_scoring_model',
               'ppr_scoring_model'
           ),
           node (
               calculate_projected_points(scoring='half_ppr'),
               ['ppr_scoring_model'],
               'projection'
           ),  
            # node(
            #     split_data,
            #     ["example_iris_data", "params:example_test_data_ratio"],
            #     dict(
            #         train_x="example_train_x",
            #         train_y="example_train_y",
            #         test_x="example_test_x",
            #         test_y="example_test_y",
            #     ),
            # )
        ]
    )
