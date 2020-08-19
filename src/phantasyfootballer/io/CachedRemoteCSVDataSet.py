from typing import Any, List, Dict, Callable, Union, Optional
import pandas as pd
from kedro.io import AbstractDataSet, DataSetError
import importlib
from pathlib import Path
import os
import datetime
import re
import logging

logger = logging.getLogger(__name__)

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


class CachedRemoteCSVDataSet(AbstractDataSet):
    
    def __init__(
        self,
        data_source: Union[Callable, str],
        expiration: str,
        local_filepath: str,
        **load_kwargs,
    ):
        """Instantiate a CSVRemote object.

        Params
        ------
        load_kwargs: Keyword arguments to pass to the data import function.
        """
        self._expiration = 24 if expiration is None else self._calculate_expiration_hours(expiration)

        self._data_source_kwargs = load_kwargs

        self._local_filepath = Path(local_filepath)

        if callable(data_source):
            self.data_source = data_source
        else:
            path_parts = data_source.split(MODULE_SEPARATOR)
            function_name = path_parts[-1]
            module_path = MODULE_SEPARATOR.join(path_parts[:-1])
            module = importlib.import_module(module_path)
            self.data_source = getattr(module, function_name)

    def _load(self) -> List[Dict[str, Any]]:
        # check last time this file was updated
        # if it is past the expiration then do the callable
        # otherwise just load the file
        file_age = self._calculate_file_age(self._local_filepath)
        data_source = None
        if file_age > self._expiration:
            logger.info(f'Cached CSV out of date {self._local_filepath}')
            data_source = self.data_source(**self._data_source_kwargs)
        else:
            logger.info(f'Cached CSV, found local {self._local_filepath}')
            data_source = pd.read_csv(self._local_filepath)
        return data_source

    def _save(self, data: pd.DataFrame) -> None:
        pass

    def _describe(self):
        return self._data_source_kwargs

    
    @staticmethod
    def _calculate_expiration_hours(expiration : Union[str,int]) -> int:
        regex = r"(\d*)\s*([H|M|D]?)"
        try:
            num, letter = re.findall(regex,'8 H')[0]
        except:
            DataSetError('Invalid expiration')
        conversion =  {'H': 1, 'D': 24, 'M': 1/60}
        return int(num * conversion.get(letter, 24))
    
    @staticmethod
    def _calculate_file_age(filepath: Path) -> int:
        '''
        Returns the age of a file in days
        '''
        today = datetime.datetime.today()
        modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
        return (today - modified_date).days/24