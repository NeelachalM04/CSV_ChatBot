from config import MAX_SAMPLE_ROWS

def summarize_result(result):

    if hasattr(result, "shape"):

        row_count = len(result)

        if row_count > MAX_SAMPLE_ROWS:

            sample = result.head(MAX_SAMPLE_ROWS)

            return {
                "rows": row_count,
                "sample": sample.to_string()
            }

    return result