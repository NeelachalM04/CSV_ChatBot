import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SAVE_LOGS = os.getenv("SAVE_LOGS", "False").lower() == "true"

LOG_DIR = "logs"


def log_query(question, query, result, status):
    """
    Save chatbot interactions into a daily Excel log file
    """

    if not SAVE_LOGS:
        return

    os.makedirs(LOG_DIR, exist_ok=True)

    # create daily log file
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(LOG_DIR, f"chatbot_{date_str}.xlsx")

    # safely convert result
    try:
        result_text = str(result)
    except Exception:
        result_text = "Unserializable result"

    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "generated_query": query,
        "result": result_text[:500],
        "status": status
    }

    try:

        if os.path.exists(log_file):
            df = pd.read_excel(log_file)
            df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
        else:
            df = pd.DataFrame([log_entry])

    except Exception:
        # fallback if file corrupted
        df = pd.DataFrame([log_entry])

    df.to_excel(log_file, index=False)