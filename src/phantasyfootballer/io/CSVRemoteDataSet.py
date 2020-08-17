from typing import Any, List, Dict, Callable, Union, Optional
import pandas as pd
from kedro.io import AbstractDataSet
import importlib

DATE_RANGE_TYPE = {
    'year': { 
        'start_year': 2019
        },
    # 'years' : {
    #     'start_year': 2000, 
    #     'end_year': 2019
    #     },
    # 'weeks' : {
    #     'start_year' : 2019,
    #}
}
MODULE_SEPARATOR = "."


class CSVRemoteDataSet(AbstractDataSet):
    
    def __init__(
        self,
        data_source: Union[Callable, str],
        date_range_type: Optional[str] = None,
        **load_kwargs,
    ):
        """Instantiate a JSONRemoteDataSet object.

        Params
        ------
        load_kwargs: Keyword arguments to pass to the data import function.
        """
        self._validate_date_range_type(date_range_type)

        self._date_range = (
            {} if date_range_type is None else DATE_RANGE_TYPE[date_range_type]
        )
        self._data_source_kwargs = {**self._date_range, **load_kwargs}

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

    @staticmethod
    def _validate_date_range_type(date_range_type: Optional[str]) -> None:
        assert date_range_type is None or date_range_type in DATE_RANGE_TYPE.keys(), (
            "Argument date_range_type must be None or one of "
            f"{DATE_RANGE_TYPE.keys()}, but {date_range_type} was received."
        )