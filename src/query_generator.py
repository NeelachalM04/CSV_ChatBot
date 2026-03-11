# Generates pandas code from natural language questions using Azure OpenAI

from src.azure_client import client
from config import AZURE_OPENAI_DEPLOYMENT


def generate_query(question, columns, categorical_values):

    prompt = f"""
You are an expert data analyst who writes Python pandas code to answer questions about tabular datasets.

A dataframe named **df** contains the dataset.

DATAFRAME COLUMNS:
{columns}

UNIQUE TEXTUAL VALUES FOR CATEGORICAL COLUMNS:
{categorical_values}

Your task is to translate the user's natural language question into valid pandas code that operates on df.

Important rules:

- Carefully check whether the user's question refers to any column in the dataset.
- Use ONLY the column names provided above.
- If the requested concept or column is not present in the dataset, return exactly:
  Requested information is not present in the dataset.

- For categorical filters, ONLY use the values listed in the UNIQUE TEXTUAL VALUES section.
- If the user refers to a categorical value using slightly different wording, choose the closest matching value from the provided list.

Examples:
User says "masters" → use "master's degree"  
User says "high school" → use "high school"  
User says "prep course completed" → use "completed"

- Do not invent new column values.
- Do not infer new metrics or combine columns unless the question explicitly asks for it.
- Return only the pandas query.
- Do NOT include markdown, or explanations.
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