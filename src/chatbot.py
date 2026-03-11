from src.csv_loader import load_csv
from src.query_generator import generate_query
from src.executor import execute_query
from src.summarizer import summarize_result
from src.response_generator import generate_response
from config import DATA_PATH


class CSVChatbot:

    def __init__(self):

        self.df = load_csv(DATA_PATH)

    def ask(self, question):

        query = generate_query(question, list(self.df.columns))
        # query = generate_query(question, list(self.df.columns))

        print("\nGenerated Query:")
        print(query)

        result = execute_query(query, self.df)

        summarized = summarize_result(result)

        answer = generate_response(question, summarized)

        return answer