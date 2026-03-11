import os
from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

MAX_SAMPLE_ROWS = 5
MAX_ROWS_DIRECT_PASS = 20
DATA_PATH = "C:\\Users\\NeelachalMohanty\\OneDrive - GyanSys Inc\\Desktop\\GENAI Assign\\CSV_BOT\\data\\StudentsPerformance.csv"