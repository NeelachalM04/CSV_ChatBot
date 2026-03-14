from src.utils.prompt_loader import get_response_prompt
from src.azure_client import client, deployment_name


def generate_response(rephrased_question, result_payload):

    prompt = get_response_prompt(rephrased_question, result_payload)

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that explains dataframe query results to users."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()