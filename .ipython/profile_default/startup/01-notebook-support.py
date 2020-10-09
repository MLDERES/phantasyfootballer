import logging.config
from pathlib import Path
from IPython.core.magic import register_line_magic

# Find the project root (./../../../)
startup_error = None
project_path = Path(__file__).parents[3].resolve()


@register_line_magic
def set_display_options():
    global current_dir
    global project_path
    global context
    global catalog
    global load_context
    global InteractiveShell
    global display
    global HTML
    global pd
    global sns
    global plt

    try:
        from pathlib import Path
        from kedro.framework.context import load_context
        from IPython.core.interactiveshell import InteractiveShell
        from IPython.display import display, HTML
        import pandas as pd
        import seaborn as sns  # noqa
        import matplotlib.pyplot as plt  # noqa
        import InteractiveShell
        import warnings

        InteractiveShell.ast_node_interactivity = "all"
        warnings.filterwarnings("ignore")
        warnings.simplefilter("ignore")

        pd.set_option("display.multi_sparse", False)
        pd.set_option("display.max_rows", 500)
        pd.set_option("precision", 4)
        # pd.set_option('display.notebook_repr_html',True)
        pd.set_option("display.precision", 4)

        current_dir = Path.cwd()  # this points to 'notebooks/' folder
        proj_path = current_dir.parent  # point back to the root of the project
        context = load_context(proj_path)
        catalog = context.catalog

    except ImportError:
        logging.error("There was a problem loading the libraries ")
        raise


def isnotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False


if isnotebook():
    set_display_options
