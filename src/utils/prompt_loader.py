import json
from langchain_core.prompts import PromptTemplate


def get_query_prompt():

    with open("src/prompts/query_prompt.jinja", "r") as f:
        template = f.read()

    return PromptTemplate(
        template=template,
        template_format="jinja2",
        input_variables=["schema", "question", "history"]
    )


def get_response_prompt():

    with open("src/prompts/response_prompt.jinja", "r") as f:
        template = f.read()

    return PromptTemplate(
        template=template,
        template_format="jinja2",
        input_variables=["question", "result"]
    )


def get_validation_prompt():

    with open("src/prompts/validation_prompt.jinja", "r") as f:
        template = f.read()

    return PromptTemplate(
        template=template,
        template_format="jinja2",
        input_variables=["rephrased_question", "query", "schema", "execution_error"]
    )