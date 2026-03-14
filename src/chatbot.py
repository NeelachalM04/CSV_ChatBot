# import pandas as pd
# import re
# import difflib
# from src.utils.csv_loader import load_csv
# from src.agents.query_agent import extract_intent_and_query   # ← updated import
# from src.agents.validation_agent import validate_query
# from src.utils.helpers import execute_query, summarize_result, normalize_result
# from src.agents.response_agent import generate_response
# from src.utils.dataframe_analyzer import analyze_dataframe


# class CSVChatbot:

#     def __init__(self):
#         self.df = load_csv()

#     def ask(self, question):

#         schema = analyze_dataframe(self.df)

#         intent, query_initial = extract_intent_and_query(question,schema)

#         print("\nExtracted Intent:")
#         print(intent)

#         retries = 0
#         max_retries = 3
#         query = query_initial.replace("```python", "").replace("```", "").strip()

#         while retries < max_retries:

#             if "|" in query or "\n|" in query:
#                 _, query = extract_intent_and_query(question, columns, categorical_values)
#                 query = query.replace("```python", "").replace("```", "").strip()
#                 retries += 1
#                 continue

#             # Step 3 → validate query
#             validation = validate_query(intent, query, columns, categorical_values)

#             if "Status: VALID" in validation:

#                 unsafe_keywords = [
#                     "drop(", "to_csv", "to_excel", "update(",
#                     "delete", "insert", "write", "save",
#                     "os.", "sys.", "subprocess"
#                 ]

#                 if any(word in query.lower() for word in unsafe_keywords):
#                     retries += 1
#                     continue

#                 if not query.strip().startswith("df"):
#                     retries += 1
#                     continue

#                 if re.search(r"^\s*\w+\s*=", query):
#                     retries += 1
#                     continue

#                 break

#             if "Corrected_Query:" in validation:
#                 query = validation.split("Corrected_Query:")[-1].strip()

#             retries += 1

#         # retries exhausted
#         if retries == max_retries:
#             available_cols = ", ".join(columns)
#             answer = (
#                 "Your request refers to a column that does not exist in the dataset. "
#                 f"Available columns are: {available_cols}. "
#                 "Please ask using one of these fields."
#             )
#             return answer, None

#         print("\nFinal Generated Query:")
#         print(query)

#         # Step 4 → execute
#         result, error = execute_query(query, self.df)

#         if result is not None:
#             result = normalize_result(result)

#         # Step 5 → handle errors
#         if error:
#             error_lower = str(error).lower()

#             if any(col_word in error_lower for col_word in ["keyerror", "not in index", "not defined"]):
#                 available_cols = ", ".join(columns)
#                 answer = (
#                     "The dataset does not contain the column referenced in your question. "
#                     f"Available columns in this dataset are: {available_cols}."
#                 )
#                 return answer, None

#             question_lower = question.lower()
#             for col, values in categorical_values.items():
#                 if col in question_lower:
#                     matches = difflib.get_close_matches(question_lower, values, n=3)
#                     if matches:
#                         suggestions = "\n".join([f"→ {v}" for v in values])
#                         answer = (
#                             f"The value mentioned in your question does not match any "
#                             f"known category in '{col}'.\n\n"
#                             f"Did you mean one of these?\n{suggestions}"
#                         )
#                         return answer, None

#             answer = generate_response(
#                 question,
#                 f"The query could not be executed due to this error: {error}"
#             )
#             return answer, None

#         # Step 6 → summarize
#         summarized = summarize_result(result)

#         # Step 7 → build response payload
#         if isinstance(summarized, dict) and "sample" in summarized:
#             response_payload = {
#                 "result": summarized["sample"],
#                 "total_rows": summarized["rows"],
#                 "display_rows": len(summarized["sample"])
#             }
#         else:
#             response_payload = {
#                 "result": summarized,
#                 "total_rows": None,
#                 "display_rows": None
#             }

#         # Step 8 → generate natural language answer
#         answer = generate_response(question, response_payload)

#         if isinstance(summarized, dict) and "sample" in summarized:
#             return answer, pd.DataFrame(summarized["sample"])

#         return answer, result


import pandas as pd
import re
import difflib

from src.utils.csv_loader import load_csv
from src.agents.query_agent import extract_intent_and_query
from src.agents.validation_agent import validate_query
from src.utils.helpers import execute_query, summarize_result, normalize_result
from src.agents.response_agent import generate_response
from src.utils.dataframe_analyzer import analyze_dataframe


class CSVChatbot:

    def __init__(self):
        self.df = load_csv()

    def ask(self, question):

        schema = analyze_dataframe(self.df)

        # Extract column names from schema
        columns = [col["column_name"] for col in schema]

        # Extract categorical columns
        categorical_values = {
            col["column_name"]: col["values"]
            for col in schema
            if col["category"]
        }

        # Step 1 → generate query
        intent, query_initial = extract_intent_and_query(question, schema)

        print("\nExtracted Intent:")
        print(intent)

        retries = 0
        max_retries = 3

        query = query_initial.replace("```python", "").replace("```", "").strip()

        while retries < max_retries:

            # guard against table outputs
            if "|" in query or "\n|" in query:
                _, query = extract_intent_and_query(question, schema)
                query = query.replace("```python", "").replace("```", "").strip()
                retries += 1
                continue

            # Step 2 → validate query
            validation = validate_query(intent, query, schema)

            if "Status: VALID" in validation:

                unsafe_keywords = [
                    "drop(", "to_csv", "to_excel", "update(",
                    "delete", "insert", "write", "save",
                    "os.", "sys.", "subprocess"
                ]

                if any(word in query.lower() for word in unsafe_keywords):
                    retries += 1
                    continue

                if not query.strip().startswith("df"):
                    retries += 1
                    continue

                if re.search(r"^\s*\w+\s*=", query):
                    retries += 1
                    continue

                break

            if "Corrected_Query:" in validation:
                query = validation.split("Corrected_Query:")[-1].strip()

            retries += 1

        # retries exhausted
        if retries == max_retries:

            available_cols = ", ".join(columns)

            answer = (
                "Your request refers to a column that does not exist in the dataset. "
                f"Available columns are: {available_cols}. "
                "Please ask using one of these fields."
            )

            return answer, None

        print("\nFinal Generated Query:")
        print(query)

        # Step 3 → execute query
        result, error = execute_query(query, self.df)

        if result is not None:
            result = normalize_result(result)

        # Step 4 → handle execution errors
        if error:

            error_lower = str(error).lower()

            if any(col_word in error_lower for col_word in ["keyerror", "not in index", "not defined"]):

                available_cols = ", ".join(columns)

                answer = (
                    "The dataset does not contain the column referenced in your question. "
                    f"Available columns in this dataset are: {available_cols}."
                )

                return answer, None

            question_lower = question.lower()

            for col, values in categorical_values.items():

                if col in question_lower:

                    matches = difflib.get_close_matches(question_lower, values, n=3)

                    if matches:

                        suggestions = "\n".join([f"→ {v}" for v in values])

                        answer = (
                            f"The value mentioned in your question does not match any "
                            f"known category in '{col}'.\n\n"
                            f"Did you mean one of these?\n{suggestions}"
                        )

                        return answer, None

            answer = generate_response(
                question,
                f"The query could not be executed due to this error: {error}"
            )

            return answer, None

        # Step 5 → summarize result
        summarized = summarize_result(result)

        # Step 6 → prepare response payload
        if isinstance(summarized, dict) and "sample" in summarized:

            response_payload = {
                "result": summarized["sample"],
                "total_rows": summarized["rows"],
                "display_rows": len(summarized["sample"])
            }

        else:

            response_payload = {
                "result": summarized,
                "total_rows": None,
                "display_rows": None
            }

        # Step 7 → generate response
        answer = generate_response(question, response_payload)

        if isinstance(summarized, dict) and "sample" in summarized:
            return answer, pd.DataFrame(summarized["sample"])

        return answer, result