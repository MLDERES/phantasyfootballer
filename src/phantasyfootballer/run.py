"""Application entry point."""
from pathlib import Path
from typing import Dict
import os
from typing import Optional
from kedro.framework.context import KedroContext, load_package_context
from kedro.pipeline import Pipeline
from phantasyfootballer.pipeline import create_pipelines
from phantasyfootballer.pipelines.full_pipeline import create_full_pipeline


class ProjectContext(KedroContext):
    """Users can override the remaining methods from the parent class here,
    or create new ones (e.g. as required by plugins)
    """

    project_name = "phantasyfootballer"
    # `project_version` is the version of kedro used to generate the project
    project_version = "0.16.4"
    package_name = "phantasyfootballer"

    def __init_(
        self, project_path: str, env: Optional[str] = os.getenv("PYTHON_ENV"), **kwargs
    ):
        super().__init__(project_path, env, **kwargs)
        ## Any other properties that need to be set for this project context, which will be shipped around - especially helpful in analysis

    @property
    def pipeline(self):
        """ Default pipeline for the PhantasyFootballer app
        """
        return create_full_pipeline()

    def _get_pipelines(self) -> Dict[str, Pipeline]:
        # TODO: Here I can override how the pipelines are created, might be helpful to set boundaries on the data used
        return create_pipelines()

    def _get_catalog(self, save_version=None, journal=None, load_versions=None):
        # TODO: This is the spot where I can add data to the catalog when instantiated
        catalog = super()._get_catalog(
            save_version=save_version, journal=journal, load_versions=load_versions
        )
        return catalog


def run_package():
    # Entry point for running a Kedro project packaged with `kedro package`
    # using `python -m <project_package>.run` command.
    project_context = load_package_context(
        project_path=Path.cwd(), package_name=Path(__file__).resolve().parent.name
    )
    project_context.run()


if __name__ == "__main__":
    run_package()
