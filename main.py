from src.chatbot import CSVChatbot
import pandas as pd

# show all columns fully
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


bot = CSVChatbot()

print("CSV Chatbot Ready (type exit to stop)")

while True:

    question = input("\nUser: ")

    if question.lower() == "exit":
        break

    answer, result = bot.ask(question)

    # Print conversational answer first
    print("\nBot:", answer)
    


    if result is not None:
        print("\nResult:")

        if isinstance(result, pd.Series):
            result = result.to_frame().T

        if isinstance(result, (pd.DataFrame, pd.Series)):
            print(result.to_string())
        else:
            print(result)
