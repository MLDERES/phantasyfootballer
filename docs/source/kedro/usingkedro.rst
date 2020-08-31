Developing with Kedro
#####################

This project has been built with `kedro`_ and therefore depends on using the `kedro <command>` to run tests, run pipelines and install dependencies.


Installing dependencies
***********************

Declare any dependencies in `src/requirements.txt` for `pip` installation and `src/environment.yml` for `conda` installation.

To install them, run:

.. code-block:: bash

    kedro install


Running Kedro
*************

You can run your Kedro project with:

.. code-block:: bash

    kedro run


Testing Kedro
****************

Have a look at the file `src/tests/test_run.py` for instructions on how to write your tests. You can run your tests with the following command:

.. code-block:: bash

    kedro test

To configure the coverage threshold, please have a look at the file `.coveragerc`.

Working with Kedro from notebooks
*********************************

In order to use notebooks in your Kedro project, you need to install Jupyter:

.. code-block:: bash

    pip install jupyter

For using Jupyter Lab, you need to install it:

.. code-block:: bash

    pip install jupyterlab


After installing Jupyter, you can start a local notebook server:

.. code-block:: bash

    kedro jupyter notebook


You can also start Jupyter Lab:

.. code-block:: bash

    kedro jupyter lab


And if you want to run an IPython session:

.. code-block:: bash

    kedro ipython


Running Jupyter or IPython this way provides the following variables in
scope: `proj_dir`, `proj_name`, `conf`, `io`, `parameters` and `startup_error`.

Converting notebook cells to nodes in a Kedro project
=====================================================

Once you are happy with a notebook, you may want to move your code over into the Kedro project structure for the next stage in your development.
This is done through a mixture of `cell tagging <https://jupyter-notebook.readthedocs.io/en/stable/changelog.html#cell-tags>`_
`kedro` and Kedro CLI commands.

By adding the `node` tag to a cell and running the command below, the cell's source code will be copied over to a Python file within `src/<package_name>/nodes/`.

.. code-block:: bash

    kedro jupyter convert <filepath_to_my_notebook>


> *Note:* The name of the Python file matches the name of the original notebook.

Alternatively, you may want to transform all your notebooks in one go. To this end, you can run the following command to convert all notebook files found in the project root directory and under any of its sub-folders.

.. code-block:: bash

    kedro jupyter convert --all


Ignoring notebook output cells in `git`
=======================================

In order to automatically strip out all output cell contents before committing to `git`, you can run `kedro activate-nbstripout`. This will add a hook in `.git/config` which will run `nbstripout` before anything is committed to `git`.

> *Note:* Your output cells will be left intact locally.

Package the project
*******************

In order to package the project's Python code in `.egg` and / or a `.wheel` file, you can run:

.. code-block:: bash

    kedro package


After running that, you can find the two packages in `src/dist/`.

Building API documentation
**************************

To build API docs for your code using Sphinx, run:

.. code-block:: bash

    kedro build-docs


See your documentation by opening `docs/build/html/index.html`.

Building the project requirements
*********************************

To generate or update the dependency requirements for your project, run:

.. code-block:: bash

    kedro build-reqs


This will copy the contents of `src/requirements.txt` into a new file `src/requirements.in` which will be used as the source for `pip-compile`. You can see the output of the resolution by opening `src/requirements.txt`.

After this, if you'd like to update your project requirements, please update `src/requirements.in` and re-run `kedro build-reqs`.

.. _kedro: https://kedro.readthedocs.io/en/stable/index.html