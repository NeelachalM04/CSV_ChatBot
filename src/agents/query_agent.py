from src.azure_client import llm
from src.utils.prompt_loader import get_query_prompt
import json
import re


def extract_intent_and_query(question, schema, history):

    prompt = get_query_prompt()

    chain = prompt | llm

    output = chain.invoke({
        "schema": json.dumps(schema, indent=2),
        "question": question,
        "history": json.dumps(history, indent=2)
    }).content.strip()

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

    if not pandas_query:
        df_match = re.search(r"(df\[[\s\S]*?\])", output)
        if df_match:
            pandas_query = df_match.group(1).strip()

    pandas_query = (
        pandas_query
        .replace("```python", "")
        .replace("```", "")
        .replace("`", "")
        .strip()
    )

    return rephrased_question, pandas_query, reasoning