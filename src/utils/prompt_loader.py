
import json
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("src/prompts"))


def get_query_prompt(schema, question, history):

    template = env.get_template("query_prompt.jinja")

    schema_text = json.dumps(schema, indent=2)
    history_text = json.dumps(history, indent=2)

    return template.render(
        schema=schema_text,
        question=question,
        history=history_text
    )


def get_response_prompt(question, result):

    template = env.get_template("response_prompt.jinja")

    return template.render(
        question=question,
        result=result
    )

def get_validation_prompt(rephrased_question, query, schema):

    template = env.get_template("validation_prompt.jinja")

    schema_text = json.dumps(schema, indent=2)

    return template.render(
        rephrased_question=rephrased_question,
        query=query,
        schema=schema_text
    )

