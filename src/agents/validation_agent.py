from src.azure_client import client, deployment_name
from src.utils.prompt_loader import get_validation_prompt


def validate_query(intent, query, schema):

    prompt = get_validation_prompt(
        intent,
        query,
        schema
    )

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {
                "role": "system",
                "content": "You validate pandas dataframe queries strictly."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()