from src.azure_client import client
from config import AZURE_OPENAI_DEPLOYMENT


def generate_query(question, columns):

    prompt = f"""
You are a pandas expert.

The dataframe name is df.

Columns:
{columns}

Generate ONLY valid pandas code.

Rules:
- Do not include explanations
- Do not include ```python
- Only return executable pandas code
- If asked for total rows use len(df)

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