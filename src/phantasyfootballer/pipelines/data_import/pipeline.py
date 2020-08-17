from kedro.pipeline import Pipeline, node

def pass_thru(input_df):
    return input_df


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                pass_thru,
                "fp_fpecr_csv_raw",
                'fp_fpecr_local'
            )
        ]
    )

