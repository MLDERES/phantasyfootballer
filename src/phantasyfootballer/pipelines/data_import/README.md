# Data Import pipeline

There are several pipelines that make up this major pipeline for all data imports including

* [data_import_pipeline](#overview)
  * [results_pipeline](#Results\ Pipeline)
    * [annual_results_pipeline](#Annual\ Results\ Pipeline)
    * [weekly_results_pipeline](#weekly_results_pipeline)
  * [projections_pipeline](#projections_pipeline)
    * [annual_projections_pipeline](#annual_projections_pipeline)
    * [weekly_projections_pipeline](#weekly_results_pipeline)

## Overview

This pipeline runs each of the other pipelines in this package

## Results Pipeline

This pipeline runs both the weekly and annual results as two nodes with no explict link between them

## Annual Results Pipeline

This pipeline concatenates all the annual results that are available together into a single file.  Additionally, if defined, it will grab the latest annual results if it is not available yet.

results.annual.source => cached_stats (results.annual.local) 
                                                              > results.annual.primary
                                      results.annual.remote 

results.annual.source => (local files with history)
results.annual.remote => (lookup for season long stats + cached stats)

### Pipeline Inputs

#### `results.annual.source`

|      |                    |
| ---- | ------------------ |
| Type | partitioned dataset |
| Description | Includes all the files that are in the `data/01_raw/results.annual/sources` folder |

### Pipeline Outputs

#### `results.annual.primary`

|      |                    |
| ---- | ------------------ |
| Type | csv file |
| Description | A single file with all the annual results from every year that is available |

## <a name='weekly_results_pipeline'></a>Weekly Results Pipeline

This pipeline concatenates all the weekly results that are available together into a single place.  Additionally, if defined, it will grab the latest weekly results if it is not available yet.

### Pipeline Inputs

#### `results.weekly.raw`

|      |                    |
| ---- | ------------------ |
| Type | csv file |
| Description | Includes all the files that are in the `data/01_raw/results.weekly/<year>/` folder |

#### `placeholder`

|      |                    |
| ---- | ------------------ |
| Type | `pandas.DataFrame` |
| Description | Data downloaded from some source that gives the weekly results |

### Pipeline Outputs

#### `results.weekly.primary`

|      |                    |
| ---- | ------------------ |
| Type | csv file |
| Description | A single file with all the weekly results from every year/week that is available |

## <a name='projections_pipeline'></a>Projections Pipeline

## <a name='annual_projections_pipeline'></a>Annual Projections Pipeline

Gathers projections from several sources and averages them together to create an annual projection.  Useful primarily in the pre/off-season

Run all of the configured projection sources (currently FantasyPros and CBS Sports), the output (or local version) of those files should be dumped into the `01_raw/projections.annual/sources` directory



### Pipeline Inputs

#### `projections.annual.cbs`

|      |                    |
| ---- | ------------------ |
| Type | `csv file` |
| Description | Go get the annual projections from [CBS Sports](https://www.cbssports.com/fantasy/football).  This is a cached reader, so if the file already exists, then just use that |


#### `projections.annual.fp`

|      |                    |
| ---- | ------------------ |
| Type | webpage |
| Description | Go get the annual projections from [FantasyPros](http://www.fantasypros.com).  This is a cached reader, so if the file already exists, then just use that |


### Pipeline Outputs

#### `projections.annual.primary`
|      |                    |
| ---- | ------------------ |
| Type | csv file |
| Description | A single file with all the weekly results from every year/week that is available |


## <a name='weekly_projections_pipeline'></a>Weekly Projections Pipeline


### Pipeline Inputs

#### `results.weekly.raw`
|      |                    |
| ---- | ------------------ |
| Type | csv file |
| Description | Includes all the files that are in the `data/01_raw/results.weekly/<year>/` folder |


#### `placeholder`

|      |                    |
| ---- | ------------------ |
| Type | `pandas.DataFrame` |
| Description | Data downloaded from some source that gives the weekly results |

### Pipeline Outputs

#### `results.weekly.primary`
|      |                    |
| ---- | ------------------ |
| Type | csv file |
| Description | A single file with all the weekly results from every year/week that is available |
