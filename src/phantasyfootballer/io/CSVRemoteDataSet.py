from typing import Any, List, Dict, Callable, Union
import pandas as pd
from kedro.io import AbstractDataSet
import importlib

MODULE_SEPARATOR = "."


class CSVRemoteDataSet(AbstractDataSet):
    def __init__(
        self, data_source: Union[Callable, str], **load_kwargs,
    ):
        """
        Instantiate a CSVRemote object.

        Params
        ------
        load_kwargs: Keyword arguments to pass to the data import function.
        """
        self._data_source_kwargs = load_kwargs

        if callable(data_source):
            self.data_source = data_source
        else:
            path_parts = data_source.split(MODULE_SEPARATOR)
            function_name = path_parts[-1]
            module_path = MODULE_SEPARATOR.join(path_parts[:-1])
            module = importlib.import_module(module_path)

            self.data_source = getattr(module, function_name)

    def _load(self) -> List[Dict[str, Any]]:
        return self.data_source(**self._data_source_kwargs)

    def _save(self, data: pd.DataFrame) -> None:
        pass

    def _describe(self):
        return self._data_source_kwargs
