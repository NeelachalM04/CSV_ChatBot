import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SAVE_LOGS = os.getenv("SAVE_LOGS", "False").lower() == "true"

LOG_DIR = "logs"


def log_query(question, query, result, status, graph_path=None):  # ⭐ ADDED: graph_path parameter
    """
    Save chatbot interactions into a daily Excel log file
    """

    if not SAVE_LOGS:
        return

    # ⭐ CHANGED: Create daily folder structure
    date_str = datetime.now().strftime("%Y-%m-%d")
    daily_logs_dir = os.path.join(LOG_DIR, date_str)
    os.makedirs(daily_logs_dir, exist_ok=True)

    # ⭐ CHANGED: Save log file inside daily folder
    log_file = os.path.join(daily_logs_dir, f"chatbot_{date_str}.xlsx")

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
        "status": status,
        "graph_path": graph_path if graph_path else ""  # ⭐ ADDED: graph path column
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