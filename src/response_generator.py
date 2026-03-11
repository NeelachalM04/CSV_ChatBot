# response generator
from src.azure_client import client
from config import AZURE_OPENAI_DEPLOYMENT

def generate_response(question, result):

    # handle sampled results
    if isinstance(result, dict) and "rows" in result and "sample" in result:
        result_text = f"""
Total rows: {result['rows']}

Showing first rows:
{result['sample']}
"""
    else:
        result_text = result

    prompt = f"""
You have been given a user's question and the result of a dataframe query, and your job is to convert that result into a clear and natural conversational response.

A dataframe query has already been executed and produced the following result.

User Question:
{question}

Query Result:
{result_text}

Instructions:

* Use the result exactly as provided.
* Do not invent additional information.
* Keep the answer concise and easy to understand.
* If the result contains multiple rows, explain what it represents and include the rows.

Return only the final answer.

"""

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content