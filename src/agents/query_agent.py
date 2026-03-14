from src.azure_client import client, deployment_name
from src.utils.prompt_loader import get_query_prompt


def extract_intent_and_query(question, schema):
    """
    Single step:
    LLM infers intent internally and generates query
    """

    query_prompt = get_query_prompt(
    schema,
    question
)

    query_response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You generate pandas queries."},
            {"role": "user", "content": query_prompt}
        ]
    )

    query = query_response.choices[0].message.content.strip()

    return question, query