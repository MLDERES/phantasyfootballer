from kedro.pipeline import Pipeline

from phantasyfootballer.pipelines import data_engineering as de


def create_full_pipeline():
    # TODO: this will be the full pipeline from getting data, to preparing the data, to setting up the features and finally executing the predictors
    return Pipeline([de.create_pipeline()])
