import yaml
import pandas as pd
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

DATA_PATH = config["dataset"]["data_path"]


def load_csv():

    df = pd.read_csv(DATA_PATH)

    # Normalize column names
    # df.columns = (
    #     df.columns
    #     .str.strip()
    #     .str.lower()
    #     .str.replace(r"[^\w\s]", "", regex=True)   # remove special chars
    #     .str.replace(" ", "_")                     # spaces → underscore
    # )

    df.columns = df.columns.str.strip()

    # Optional short aliases for cleaner queries
    df.rename(columns={
        "parental_level_of_education": "parent_edu",
        "test_preparation_course": "prep_course"
    }, inplace=True)

    return df