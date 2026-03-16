# import pandas as pd
# import yaml
# from pathlib import Path

# # load config.yaml
# CONFIG_PATH = Path("config.yaml")

# with open(CONFIG_PATH, "r") as f:
#     config = yaml.safe_load(f)

# analysis_config = config["dataframe_analysis"]

# def analyze_dataframe(df):
#     """
#     Deterministically analyze dataframe schema.

#     Returns structured schema for LLM usage.
#     """

#     schema = {
#         "categorical_columns": {},
#         "numerical_columns": [],
#         "datetime_columns": [],
#         "other_columns": []
#     }

#     total_rows = max(len(df), 1)

#     for col in df.columns:

#         series = df[col]
#         dtype = series.dtype

#         unique_values = series.dropna().unique()
#         unique_count = len(unique_values)

#         unique_ratio = unique_count / total_rows

#         # datetime detection
#         if pd.api.types.is_datetime64_any_dtype(dtype):

#             schema["datetime_columns"].append(col)

#         # ID / high cardinality detection
#         elif unique_ratio >= analysis_config["id_threshold"]:

#             schema["other_columns"].append(col)

#         # categorical detection
#         elif (
#             dtype == "object"
#             or dtype.name == "category"
#             or dtype == "bool"
#             or unique_count <= analysis_config["unique_threshold"]
#             or unique_ratio <= analysis_config["ratio_threshold"]
#         ):

#             schema["categorical_columns"][col] = [
#                 str(v) for v in unique_values[:analysis_config["max_categorical_values"]]
#             ]

#         # numerical columns
#         elif pd.api.types.is_numeric_dtype(dtype):

#             schema["numerical_columns"].append(col)

#         # fallback
#         else:

#             schema["other_columns"].append(col)

#     return schema



import pandas as pd
import yaml
from pathlib import Path

CONFIG_PATH = Path("config.yaml")

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

analysis_config = config["dataframe_analysis"]


def analyze_dataframe(df):
    """
    Analyze dataframe schema and return structured column metadata.
    Works for any dataset.
    """

    schema = []
    total_rows = max(len(df), 1)

    for col in df.columns:

        series = df[col]
        dtype = series.dtype

        unique_values = series.dropna().unique()
        unique_count = len(unique_values)
        unique_ratio = unique_count / total_rows

        # Detect column type
        if pd.api.types.is_integer_dtype(dtype):
            col_type = "int"
        elif pd.api.types.is_float_dtype(dtype):
            col_type = "float"
        elif pd.api.types.is_bool_dtype(dtype):
            col_type = "bool"
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            col_type = "datetime"
        # elif dtype == "object":
    
        #     sample_values = series.dropna().astype(str).head(5)

        #     if all(pd.to_datetime(sample_values, format="%m/%d/%Y", errors="coerce").notna()):
        #         col_type = "date"

        #     elif all(pd.to_datetime(sample_values, format="%H:%M", errors="coerce").notna()):
        #         col_type = "time"

        #     else:
        #         col_type = "string"
        else:
            col_type = "string"

        # Detect categorical
        is_categorical = False

        if (
            dtype == "object"
            or dtype.name == "category"
            or unique_count <= analysis_config["unique_threshold"]
            or unique_ratio <= analysis_config["ratio_threshold"]
        ):
            is_categorical = True

        if unique_ratio >= analysis_config["id_threshold"]:
            is_categorical = False

        # Sample values (for LLM context)
        if is_categorical:
            values = [str(v) for v in unique_values[:analysis_config["max_categorical_values"]]]
        else:
            values = [str(v) for v in unique_values[:5]]

        column_schema = {
            "column_name": col,
            "category": is_categorical,
            "values": values,
            "type": col_type
        }

        schema.append(column_schema)

    return schema