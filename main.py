
from src.chatbot import CSVChatbot
import os
from dotenv import load_dotenv
load_dotenv()

bot = CSVChatbot()

print("CSV Chatbot Ready (type exit to stop)")

while True:

    question = input("\nUser: ")

    if question.lower() == "exit":
        break

    answer = bot.ask(question)

    print("\nBot:", answer)