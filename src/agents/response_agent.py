
from src.utils.prompt_loader import get_response_prompt
from src.azure_client import client, deployment_name


def generate_response(question, result_text):

    prompt = get_response_prompt(question, result_text)

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You explain query results clearly."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()