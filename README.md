# phantasyfootballer

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![forks](https://img.shields.io/github/forks/MLDERES/phantasyfootballer)
![stars](https://img.shields.io/github/stars/MLDERES/phantasyfootballer)


## Overview

This is project dedicated to gathering and analyzing data for the purposes of crushing my leagues in fantasy football.

This was a project generated with [Kedro](https://kedro.readthedocs.io), which helps to enforce good data engineering
[convention](https://kedro.readthedocs.io/en/stable/06_resources/01_faq.html#what-is-data-engineering-convention)

## Installing dependencies

Declare any dependencies in `src/requirements.txt` for `pip` installation and `src/environment.yml` for `conda` installation.

To install them, run:

```bash
kedro install
```

## Running Kedro

You can run your Kedro project with:

```bash
kedro run
```

## Testing Kedro

Have a look at the file `src/tests/test_run.py` for instructions on how to write your tests. You can run your tests with the following command:

```bash
kedro test
```

To configure the coverage threshold, please have a look at the file `.coveragerc`.

## Working with Kedro from notebooks

In order to use notebooks in your Kedro project, you need to install Jupyter:

```bash
pip install jupyter
```

For using Jupyter Lab, you need to install it:

```bash
pip install jupyterlab
```

After installing Jupyter, you can start a local notebook server:

```bash
kedro jupyter notebook
```

You can also start Jupyter Lab:

```sh
kedro jupyter lab
```

And if you want to run an IPython session:

```sh
kedro ipython
```

Running Jupyter or IPython this way provides the following variables in
scope: `proj_dir`, `proj_name`, `conf`, `io`, `parameters` and `startup_error`.

### Converting notebook cells to nodes in a Kedro project

Once you are happy with a notebook, you may want to move your code over into the Kedro project structure for the next stage in your development. This is done through a mixture of [cell tagging](https://jupyter-notebook.readthedocs.io/en/stable/changelog.html#cell-tags) and Kedro CLI commands.

By adding the `node` tag to a cell and running the command below, the cell's source code will be copied over to a Python file within `src/<package_name>/nodes/`.

```sh
kedro jupyter convert <filepath_to_my_notebook>
```

> *Note:* The name of the Python file matches the name of the original notebook.

Alternatively, you may want to transform all your notebooks in one go. To this end, you can run the following command to convert all notebook files found in the project root directory and under any of its sub-folders.

```sh
kedro jupyter convert --all
```

### Ignoring notebook output cells in `git`

In order to automatically strip out all output cell contents before committing to `git`, you can run `kedro activate-nbstripout`. This will add a hook in `.git/config` which will run `nbstripout` before anything is committed to `git`.

> *Note:* Your output cells will be left intact locally.

## Package the project

In order to package the project's Python code in `.egg` and / or a `.wheel` file, you can run:

```sh
kedro package
```

After running that, you can find the two packages in `src/dist/`.

## Building API documentation

To build API docs for your code using Sphinx, run:

```sh
kedro build-docs
```

See your documentation by opening `docs/build/html/index.html`.

## Building the project requirements

To generate or update the dependency requirements for your project, run:

```sh
kedro build-reqs
```

This will copy the contents of `src/requirements.txt` into a new file `src/requirements.in` which will be used as the source for `pip-compile`. You can see the output of the resolution by opening `src/requirements.txt`.

After this, if you'd like to update your project requirements, please update `src/requirements.in` and re-run `kedro build-reqs`.
