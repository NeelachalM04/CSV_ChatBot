import re
import json
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')   # opens popup window from CMD
import matplotlib.pyplot as plt
from src.azure_client import llm
from src.utils.prompt_loader import get_graph_prompt
import os                      
from datetime import datetime


def decide_and_plot(question, result):  #fun called in main
    """
    Decides if a graph is needed based on question + result.
    If yes, plots the appropriate graph type.
    Works with any dataset.
    Returns: filepath of saved graph, or None if no graph created
    """

    # only process DataFrame or Series — skip scalars
    if not isinstance(result, (pd.DataFrame, pd.Series)):
        return

    # convert result to readable string for LLM
    try:
        if isinstance(result, pd.DataFrame):
            result_text = result.to_string(index=True, max_rows=20)
        else:
            result_text = result.to_string()
    except Exception:
        result_text = str(result)

    # Step 1 → ask LLM if graph is needed and which type
    try:
        prompt = get_graph_prompt()
        chain = prompt | llm

        output = chain.invoke({
            "question": question,
            "result": result_text
        }).content.strip()

        print("\nGraph Decision:")
        print(output)

    except Exception as e:
        print(f"\n[Graph agent failed: {e}]")
        return

    # Step 2 → parse LLM response
    graph_needed = _extract(output, "Graph_Needed")
    graph_type   = _extract(output, "Graph_Type").lower()
    x_col        = _extract(output, "X_Column")
    y_col        = _extract(output, "Y_Column")
    title        = _extract(output, "Title")

    if graph_needed.lower() != "yes":
        print("\n[No graph needed for this result]")
        return None  #  CHANGED: return None instead of just return

    print(f"\n[Generating {graph_type} chart: {title}]")

    # Step 3 → build and display the graph
    filepath = _plot(result, graph_type, x_col, y_col, title)  #  CHANGED: capture filepath
    return filepath  #  ADDED: return the filepath


def _extract(text, field):
    """Safely extract a field value from LLM structured output"""
    match = re.search(rf"{field}:\s*(.*)", text)
    return match.group(1).strip() if match else "none"


def _plot(result, graph_type, x_col, y_col, title):
    """
    Plots the graph and saves it to logs folder.
    Returns: filepath of saved graph
    """
    filepath = None

    try:
        # safety: always reset index so named index becomes a real column
        if isinstance(result, pd.DataFrame):
            if not isinstance(result.index, pd.RangeIndex):
                result = result.reset_index()  # "Product line" index → becomes column

        elif isinstance(result, pd.Series):
            # convert Series to DataFrame — index becomes a column
            result = result.reset_index()
            result.columns = [result.columns[0], "count"]

        print(f"[Plot] Type: {graph_type} | X: {x_col} | Y: {y_col}")
        print(f"[Plot] Available columns after reset: {result.columns.tolist()}")

        fig, ax = plt.subplots(figsize=(10, 6))

        # get actual string and numeric columns after reset
        str_cols = result.select_dtypes(include="object").columns.tolist()
        num_cols = result.select_dtypes(include="number").columns.tolist()

        # ---- BAR CHART ----
        if graph_type == "bar":

            # check if LLM-suggested columns exist after reset
            x = x_col if (x_col != "none" and x_col in result.columns) else (str_cols[0] if str_cols else None)
            y = y_col if (y_col != "none" and y_col in result.columns) else (num_cols[0] if num_cols else None)

            print(f"[Plot] Using X: {x} | Y: {y}")

            if x and y:
                result.plot(kind="bar", x=x, y=y, ax=ax, color="steelblue", edgecolor="black", legend=False)
                ax.set_xlabel(x)
                ax.set_ylabel(y)
            elif num_cols:
                result[num_cols[0]].plot(kind="bar", ax=ax, color="steelblue", edgecolor="black")
                ax.set_ylabel(num_cols[0])

        # ---- LINE CHART ----
        elif graph_type == "line":

            x = x_col if (x_col != "none" and x_col in result.columns) else (str_cols[0] if str_cols else None)
            y = y_col if (y_col != "none" and y_col in result.columns) else (num_cols[0] if num_cols else None)

            if x and y:
                result.plot(kind="line", x=x, y=y, ax=ax, marker="o", color="steelblue", legend=False)
                ax.set_xlabel(x)
                ax.set_ylabel(y)
            elif num_cols:
                result[num_cols[0]].plot(kind="line", ax=ax, marker="o", color="steelblue")

        # ---- PIE CHART ----
        elif graph_type == "pie":

            x = x_col if (x_col != "none" and x_col in result.columns) else (str_cols[0] if str_cols else None)
            y = y_col if (y_col != "none" and y_col in result.columns) else (num_cols[0] if num_cols else None)

            if x and y:
                result.set_index(x)[y].plot(kind="pie", ax=ax, autopct="%1.1f%%", startangle=90)
                ax.set_ylabel("")
            elif str_cols and num_cols:
                result.set_index(str_cols[0])[num_cols[0]].plot(kind="pie", ax=ax, autopct="%1.1f%%")
                ax.set_ylabel("")

        # ---- HISTOGRAM ----
        elif graph_type == "histogram":

            col = y_col if (y_col != "none" and y_col in result.columns) else (num_cols[0] if num_cols else None)

            if col:
                result[col].plot(kind="hist", ax=ax, bins=20, color="steelblue", edgecolor="black")
                ax.set_xlabel(col)
                ax.set_ylabel("Frequency")

        # ---- SCATTER PLOT ----
        elif graph_type == "scatter":

            x = x_col if (x_col != "none" and x_col in result.columns) else (num_cols[0] if len(num_cols) >= 2 else None)
            y = y_col if (y_col != "none" and y_col in result.columns) else (num_cols[1] if len(num_cols) >= 2 else None)

            if x and y:
                ax.scatter(result[x], result[y], color="steelblue", alpha=0.6, edgecolors="black")
                ax.set_xlabel(x)
                ax.set_ylabel(y)

        else:
            print(f"[Unknown graph type: {graph_type}]")
            plt.close()
            return

        # final formatting
        ax.set_title(title, fontsize=13, fontweight="bold", pad=15)
        plt.xticks(rotation=45, ha="right", fontsize=9)
        plt.tight_layout()
        
        # ⭐ SAVE GRAPH TO DAILY FOLDER ⭐
        date_str = datetime.now().strftime("%Y-%m-%d")
        time_str = datetime.now().strftime("%H%M%S")
        
        # Create daily folder structure: logs/YYYY-MM-DD/graphs/
        daily_logs_dir = os.path.join("logs", date_str)
        graphs_dir = os.path.join(daily_logs_dir, "graphs")
        os.makedirs(graphs_dir, exist_ok=True)
        
        # Save with timestamp as filename
        filename = f"{time_str}.png"
        filepath = os.path.join(graphs_dir, filename)
        
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"\n[Graph saved to: {filepath}]")
        
        plt.show(block=False)   # ← non-blocking, doesn't pause code
        plt.pause(0.5)          # ← small pause to render the window

    except Exception as e:
        print(f"[Graph plotting failed: {e}]")
        import traceback
        traceback.print_exc()
        plt.close()
        return None  # ⭐ ADDED: return None if plotting failed
    
    return filepath  # ⭐ ADDED: return filepath on success