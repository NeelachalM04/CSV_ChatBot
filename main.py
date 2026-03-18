# from src.chatbot import CSVChatbot
# import pandas as pd

# # show all columns fully
# pd.set_option('display.max_columns', None)   # show ALL columns
# pd.set_option('display.width', None)          # no line wrap
# pd.set_option('display.max_colwidth', None)   # no content cut off


# bot = CSVChatbot()

# print("CSV Chatbot Ready (type exit to stop)")

# while True:

#     question = input("\nUser: ")

#     if question.lower() == "exit":
#         break

#     answer, result = bot.ask(question)

#     # Print conversational answer first
#     print("\nBot:", answer)
    


#     if result is not None:
#         print("\nResult:")

#         if isinstance(result, pd.Series):
#             result = result.to_frame().T

#         if isinstance(result, (pd.DataFrame, pd.Series)):
#             print(result.to_string())
#         else:
#             print(result)
    
#       

from src.chatbot import CSVChatbot
from src.agents.graph_agent import decide_and_plot
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

bot = CSVChatbot()

print("CSV Chatbot Ready (type exit to stop)")

while True:

    question = input("\nUser: ")

    if question.lower() == "exit":
        break

    # ⭐ CHANGED: Receive dictionary with all data
    data = bot.ask(question)
    
    answer = data['answer']
    result = data['result']
    rephrased_question = data['rephrased_question']
    graph_result = data['graph_result']     #The data to be used for graphing
    query = data['query']
    error = data['error']

    # Step 1 → print answer first
    print("\nBot:", answer)

    # Step 2 → print result table
    if result is not None:
        print("\nResult:")

        if isinstance(result, pd.Series):
            result = result.to_frame().T

        if isinstance(result, (pd.DataFrame, pd.Series)):
            print(result.to_string())
        else:
            print(result)

    # Step 3 → show graph LAST and capture filepath
    graph_filepath = None
    if graph_result is not None:
        graph_filepath = decide_and_plot(rephrased_question, graph_result)

    # Step 4 → Log interaction with graph path
    from src.utils.log_func import log_query
    
    if error:
        log_query(rephrased_question, query, error, "FAILED", graph_path=None)
    else:
        log_query(rephrased_question, query, result, "SUCCESS", graph_path=graph_filepath)