def execute_query(code, df):

    try:
        result = eval(code, {"df": df})
        return result, None

    except Exception as e:
        return None, str(e)