"""
This module contains an example test.

Tests should be placed in ``src/tests``, in modules that mirror your
project's structure, and in files named test_*.py. They are simply functions
named ``test_*`` which test a unit of logic.

To run the tests, run ``kedro test``.
"""


def test_project_name(project_context):
    assert project_context.project_name == "phantasyfootballer"


def test_project_version(project_context):
    assert project_context.project_version == "0.16.4"
