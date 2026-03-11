# Orchestrates the entire flow of the chatbot
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

        columns = list(self.df.columns)

        # extract unique textual values (ignore numerical columns)
        categorical_values = {}

        for col in self.df.columns:
            if self.df[col].dtype == "object":
                categorical_values[col] = list(self.df[col].dropna().unique())[:10]

        query = generate_query(question, columns, categorical_values)

        # clean markdown if present
        query = query.replace("```python", "").replace("```", "").strip()

        print("\nGenerated Query:")
        print(query)

        
        # execute only if it looks like pandas code
        if not any(keyword in query for keyword in ["df", "len(", ".mean()", ".max()", ".min()", ".groupby("]):
            query = None

        if query is None:
            return "Requested information is not present in the dataset."

        result = execute_query(query, self.df)

        summarized = summarize_result(result)

        answer = generate_response(question, summarized)

        return answer