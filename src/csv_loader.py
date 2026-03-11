import pandas as pd

def load_csv(path):
    df = pd.read_csv(path)
    # df.columns = df.columns.str.strip()
    df.columns = df.columns.str.strip().str.lower()
    return df