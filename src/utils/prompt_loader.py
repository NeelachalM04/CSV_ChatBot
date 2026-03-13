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




from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("src/prompts"))


def get_query_prompt(columns, categorical_values, intent):

    template = env.get_template("query_prompt.jinja")

    return template.render(
        columns=columns,
        categorical_values=categorical_values,
        intent=intent
    )


def get_response_prompt(question, result):

    template = env.get_template("response_prompt.jinja")

    return template.render(
        question=question,
        result=result
    )

def get_validation_prompt(intent, query, columns, categorical_values):
   
    template = env.get_template("validation_prompt.jinja")
    return template.render(
        intent=intent,
        query=query,
        columns=columns,
        categorical_values=categorical_values
    )

