import os
import pandas as pd

HISTORY_DIR = "history"
HISTORY_FILE = os.path.join(HISTORY_DIR, "conversation_history.csv")

MAX_HISTORY_ROWS = 200


def save_history(question, answer):

    os.makedirs(HISTORY_DIR, exist_ok=True)

    entry = {
        "question": question,
        "answer": answer
    }

    if os.path.exists(HISTORY_FILE):

        df = pd.read_csv(HISTORY_FILE)
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)

    else:

        df = pd.DataFrame([entry])

    if len(df) > MAX_HISTORY_ROWS:
        df = df.tail(MAX_HISTORY_ROWS)

    df.to_csv(HISTORY_FILE, index=False)


def get_recent_history(n=3):

    if not os.path.exists(HISTORY_FILE):
        return []

    df = pd.read_csv(HISTORY_FILE)

    recent = df.tail(n)

    history = []

    for _, row in recent.iterrows():
        history.append({
            "question": row["question"],
            "answer": row["answer"]
        })

    return history