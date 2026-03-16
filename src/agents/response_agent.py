from src.azure_client import llm
from src.utils.prompt_loader import get_response_prompt


def generate_response(rephrased_question, result_payload):

    prompt = get_response_prompt()

    chain = prompt | llm

    response = chain.invoke({
        "question": rephrased_question,
        "result": result_payload
    }).content

    return response.strip()