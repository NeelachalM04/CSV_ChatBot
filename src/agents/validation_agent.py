from src.azure_client import llm
from src.utils.prompt_loader import get_validation_prompt
import json


def validate_query(rephrased_question, query, schema):

    prompt = get_validation_prompt()

    chain = prompt | llm

    response = chain.invoke({
        "rephrased_question": rephrased_question,
        "query": query,
        "schema": json.dumps(schema, indent=2)
    }).content

    return response.strip()