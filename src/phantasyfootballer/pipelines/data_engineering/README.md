# Data Engineering pipeline

## Overview

This pipeline takes care of several tasks related to cleaning data and adding in features.

## Pipeline inputs

### `example_iris_data`

|      |                    |
| ---- | ------------------ |
| Type | `pandas.DataFrame` |
| Description | Input data to split into train and test sets |

### `params:example_test_data_ratio`

|      |                    |
| ---- | ------------------ |
| Type | `float` |
| Description | The split ratio parameter that identifies what percentage of rows goes to the train set |

## Pipeline outputs

### ``

|      |                    |
| ---- | ------------------ |
| Type | `pandas.DataFrame` |
| Description | DataFrame containing train set features |
