# from src.utils.config_loader import load_config

# config = load_config()
# MAX_SAMPLE_ROWS = config["limits"]["max_sample_rows"]


# def execute_query(code, df):

#     try:
#         result = eval(code, {"df": df})
#         return result, None

#     except Exception as e:
#         return None, str(e)


# def summarize_result(result):

#     # If result is a dataframe
#     if hasattr(result, "shape"):

#         row_count = len(result)

#         if row_count > MAX_SAMPLE_ROWS:

#             sample = result.head(MAX_SAMPLE_ROWS)

#             return {
#                 "rows": row_count,
#                 "sample": sample.to_dict(orient="records")      # convert sample() to list of dicts for better readability
#             }

#         # small dataframe → return full data
#         return result.to_dict(orient="records")

#     return result



import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MAX_SAMPLE_ROWS = config["limits"]["max_sample_rows"]


def execute_query(code, df):

    try:
        result = eval(code, {"df": df})
        return result, None

    except Exception as e:
        return None, str(e)


def summarize_result(result):

    # ---- CASE 1: DataFrame ----
    if hasattr(result, "shape") and hasattr(result, "columns"):

        row_count = len(result)

        if row_count > MAX_SAMPLE_ROWS:

            sample = result.head(MAX_SAMPLE_ROWS)

            return {
                "rows": row_count,
                "sample": sample.to_dict(orient="records")
            }

        return result.to_dict(orient="records")

    # ---- CASE 2: Series (e.g. value_counts, groupby results) ----
    if hasattr(result, "to_dict"):

        data = result.to_dict()

        if len(data) > MAX_SAMPLE_ROWS:
            data = dict(list(data.items())[:MAX_SAMPLE_ROWS])

        return data

    # ---- CASE 3: Scalar (min, max, mean, etc.) ----
    return result

import pandas as pd
import numpy as np


def normalize_result(result):

    # scalar results (min, max, mean, etc.)
    if isinstance(result, (int, float, str, np.integer, np.floating)):
        return result

    # pandas series
    if isinstance(result, pd.Series):
        return result.to_frame(name=result.name if result.name else "value")

    # pandas dataframe
    if isinstance(result, pd.DataFrame):

        # convert index to column if meaningful
        if not isinstance(result.index, pd.RangeIndex):
            result = result.reset_index()
        return result

    # numpy array or list
    if isinstance(result, (list, np.ndarray)):
        return pd.DataFrame({"value": list(result)})

    # dictionary
    if isinstance(result, dict):
        return pd.DataFrame(list(result.items()), columns=["key", "value"])
    return result