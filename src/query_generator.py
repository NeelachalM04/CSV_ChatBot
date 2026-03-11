from src.azure_client import client
from config import AZURE_OPENAI_DEPLOYMENT


def generate_query(question, columns):

    prompt = f"""
You are an expert data analyst who writes Python pandas code to answer questions about tabular datasets.

A dataframe named **df** contains the dataset.

DATAFRAME COLUMNS:
{columns}

Your task is to translate the user's natural language question into valid pandas code that operates on df.

Important rules:
- Carefully check whether the user's question refers to any column in the dataset.
- If the requested concept or column is not present in the dataset, return exactly:
   Requested information is not present in the dataset.
- Do not infer new metrics or combine columns unless the question explicitly asks for it.
- Use only the columns listed above.
- Return only the pandas query.
- Do NOT include markdown, backticks, or explanations.
- Output must be a single executable Python expression.


User Question:
{question}

"""

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content.strip()