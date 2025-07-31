import os
import pandas as pd
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

def get_llm():
    return ChatGoogleGenerativeAI(model="gemini-2.5-pro")

def generate_pandas_code(llm, question: str, df=None, history: str = "") -> str:
    columns_snippet = ""
    if df is not None:
        col_lines = []
        for col in df.columns:
            safe_col = col.replace("{", "{{").replace("}", "}}")
            sample = None
            for val in df[col]:
                if pd.notnull(val):
                    sample = val
                    break
            sample_str = f"(example: {sample})" if sample is not None else ""
            col_lines.append(f"- {safe_col} {sample_str}")
        columns_snippet = (
            "The DataFrame has the following columns:\n"
            + "\n".join(col_lines)
            + "\n\n"
        )
    safe_history = history.replace("{", "{{").replace("}", "}}") if history else ""
    history_block = f"Conversation so far:\n{safe_history}\n\n" if safe_history else ""

    prompt_template = (
        f"{columns_snippet}"
        "You are a data assistant working with a pandas DataFrame named 'df' and Plotly Express imported as 'px'.\n"
        f"{history_block}"
        "When generating code, use the exact columns above and reference previous conversation context as needed. "
        "If the user's input uses simplified or natural language terms for columns, choose the nearest matching column.\n"
        "Do NOT include import statements or markdown fences. "
        "If the user requests data cleaning, modify or reassign 'df'. "
        "If a chart or plot is requested, assign the Plotly figure to 'fig'. "
        "For other queries, assign the output to 'result'. "
        "Return only valid Python code without any extra text.\n\n"
        "User: {question}\n"
        "Assistant:"
    )

    prompt = PromptTemplate(input_variables=["question"], template=prompt_template)
    formatted_prompt = prompt.format(question=question)
    response = llm.invoke(formatted_prompt)
    code_str = response.content.strip() if hasattr(response, "content") else str(response).strip()
    return code_str

def log_audit(audit_log: list, user_input: str, code: str, status: str, comment: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = {
        "timestamp": timestamp,
        "input": user_input,
        "code": code,
        "status": status,
        "comment": comment
    }
    audit_log.append(record)
    return audit_log
