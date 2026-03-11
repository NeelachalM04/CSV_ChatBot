from src.azure_client import client
from config import AZURE_OPENAI_DEPLOYMENT

def generate_response(question, result):

    prompt = f"""
User Question:
{question}

Result from dataset:
{result}

Generate a conversational answer.
"""

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content