# from src.azure_client import client, deployment_name
# from src.utils.prompt_loader import get_query_prompt
# import re


# def extract_intent_and_query(question, schema, history):

#     query_prompt = get_query_prompt(
#         schema,
#         question,
#         history
#     )

#     query_response = client.chat.completions.create(
#         model=deployment_name,
#         messages=[
#             {"role": "system", "content": "You generate pandas queries."},
#             {"role": "user", "content": query_prompt}
#         ]
#     )

#     output = query_response.choices[0].message.content.strip()

#     # --------------------------------
#     # Parse structured COT output
#     # --------------------------------

#     rephrased_question = question
#     pandas_query = ""
#     reasoning = ""

#     rq_match = re.search(r"Rephrased_Question:\s*(.*)", output)
#     pq_match = re.search(r"Pandas_Query:\s*(.*)", output)
#     rs_match = re.search(r"Reasoning:\s*(.*)", output, re.DOTALL)

#     if rq_match:
#         rephrased_question = rq_match.group(1).strip()

#     if pq_match:
#         pandas_query = pq_match.group(1).strip()

#     if rs_match:
#         reasoning = rs_match.group(1).strip()

#     return rephrased_question, pandas_query, reasoning


from src.azure_client import client, deployment_name
from src.utils.prompt_loader import get_query_prompt
import re


def extract_intent_and_query(question, schema, history):

    query_prompt = get_query_prompt(
        schema,
        question,
        history
    )

    query_response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You generate pandas dataframe queries."},
            {"role": "user", "content": query_prompt}
        ]
    )

    output = query_response.choices[0].message.content.strip()

    # --------------------------------
    # Parse structured COT output
    # --------------------------------

    rephrased_question = question
    pandas_query = ""
    reasoning = ""

    rq_match = re.search(r"Rephrased_Question:\s*(.*)", output)
    pq_match = re.search(r"Pandas_Query:\s*([\s\S]*?)(?:\nReasoning:|$)", output)
    rs_match = re.search(r"Reasoning:\s*([\s\S]*)", output)

    if rq_match:
        rephrased_question = rq_match.group(1).strip()

    if pq_match:
        pandas_query = pq_match.group(1).strip()

    if rs_match:
        reasoning = rs_match.group(1).strip()

    # --------------------------------
    # Fallback query extraction
    # --------------------------------

    if not pandas_query:
        df_match = re.search(r"(df\[[\s\S]*?\])", output)
        if df_match:
            pandas_query = df_match.group(1).strip()

    # Remove markdown formatting if present
    pandas_query = (
        pandas_query
        .replace("```python", "")
        .replace("```", "")
        .replace("`", "")
        .strip()
    )

    return rephrased_question, pandas_query, reasoning