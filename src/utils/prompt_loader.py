# from jinja2 import Environment, FileSystemLoader


# env = Environment(loader=FileSystemLoader("src/prompts"))


# def get_query_prompt(columns, categorical_values, question):

#     template = env.get_template("query_prompt.jinja")

#     return template.render(
#         columns=columns,
#         categorical_values=categorical_values,
#         question=question
#     )


# def get_response_prompt(question, result):

#     template = env.get_template("response_prompt.jinja")

#     return template.render(
#         question=question,
#         result=result
#     )



import json
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("src/prompts"))

def get_query_prompt(schema, question):

    template = env.get_template("query_prompt.jinja")

    # convert schema to formatted JSON for better LLM understanding
    schema_text = json.dumps(schema, indent=2)

    return template.render(
        schema=schema_text,
        question=question
    )


def get_response_prompt(question, result):

    template = env.get_template("response_prompt.jinja")

    return template.render(
        question=question,
        result=result
    )

def get_validation_prompt(intent, query, schema):

    template = env.get_template("validation_prompt.jinja")

    schema_text = json.dumps(schema, indent=2)

    return template.render(
        intent=intent,
        query=query,
        schema=schema_text
    )

