from src.azure_client import client, deployment_name
from src.utils.prompt_loader import get_validation_prompt


def validate_query(rephrased_question, query, schema):

    prompt = get_validation_prompt(
        rephrased_question,
        query,
        schema
    )

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {
                "role": "system",
                "content": "You are a strict validator for pandas dataframe queries."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()