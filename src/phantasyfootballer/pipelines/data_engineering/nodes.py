# Copyright 2020 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.
"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

PLEASE DELETE THIS FILE ONCE YOU START WORKING ON YOUR OWN PROJECT!
"""

from typing import Any, Dict
from phantasyfootballer.settings import *
import pandas as pd
from kedro.config import ConfigLoader
from functools import reduce, partial, update_wrapper

def _pts_col(scoring):
    return f'{scoring}_pts'

def _pos_rank_col(scoring):
    return f'{scoring}_rank'

def normalize_data_source(data : pd.DataFrame, stat_name: str, common_stats : Dict[str, any]) -> pd.DataFrame:
    """
    This node will take a data source that is provided and adjust the stats so that they have 
    a common stat column name.  Additionally, if there is a stat that is common to the entire dataset
    (e.g. NFL week, NFL year, all qbs) that isn't already part of the file then this will be set as well.

    Say for instance, that the provider returns a file called 2019_passing_stats.  The column NFL Year is
    not likley included, so you can have it included by specifying that in the common_stats dictionary.

    The mapping from a provider column name and the common name are taking from conf/project/parameters.yml
    """
    pass

def establish_position_rank(data):
    '''
    This node will create a position rank based on projections
    '''
    pass

def _craft_scoring_dict(scheme):
    '''
    Look up the scoring system in the scoring.yml file and then merge the dictionary with the
    standard
    '''
    conf_paths = ['conf/base', 'conf/local']
    conf_loader = ConfigLoader(conf_paths)
    conf_scoring = conf_loader.get("scoring*")

    def_scoring = conf_scoring['default']
    scheme_scoring = conf_scoring.get(scheme,{})
    def_scoring.update(scheme_scoring)
    return def_scoring
    
def _calculate_projected_points(scoring, data):
    score_map = _craft_scoring_dict(scoring)
    df_pts = pd.DataFrame()
    for c in data.columns:
        if (m := score_map.get(c)):
            df_pts[c+'_pts'] = data[c]*m
    data[_pts_col(scoring)] = df_pts.sum(axis=1)

    return data

def calculate_projected_points(scoring: str) -> pd.DataFrame :
    return update_wrapper(partial(_calculate_projected_points, scoring), _calculate_projected_points)    

def _calculate_position_rank(scoring, data):
    data[_pos_rank_col(scoring)] = df_pos[_pts_col(scoring)].rank(na_option='bottom',ascending=False)
    return data

def calculate_position_rank(scoring):
    return update_wrapper( partial(_calculate_position_rank, scoring), 
        _calculate_position_rank)    

    
    