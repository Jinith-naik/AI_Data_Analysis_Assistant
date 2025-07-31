import streamlit as st
import pandas as pd
import plotly.express as px
import io
from langchain.memory import ConversationBufferMemory
from llm_utils import get_llm, generate_pandas_code, log_audit

def clean_code(code_str: str) -> str:
    lines = code_str.strip().split('\n')
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return '\n'.join(lines).strip()

def initialize_states():
    if "df" not in st.session_state:
        st.session_state.df = None
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(return_messages=False)
    if "df_history" not in st.session_state:
        st.session_state.df_history = []
    if "df_future" not in st.session_state:
        st.session_state.df_future = []
    if "audit_log" not in st.session_state:
        st.session_state.audit_log = []

def push_to_history(df):
    st.session_state.df_history.append(df.copy())
    st.session_state.df_future = []

def undo():
    if st.session_state.df_history:
        st.session_state.df_future.append(st.session_state.df.copy())
        st.session_state.df = st.session_state.df_history.pop()

def redo():
    if st.session_state.df_future:
        st.session_state.df_history.append(st.session_state.df.copy())
        st.session_state.df = st.session_state.df_future.pop()

def audit_log_csv(audit_log):
    import csv
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["timestamp", "input", "code", "status", "comment"])
    writer.writeheader()
    for row in audit_log:
        writer.writerow(row)
    return output.getvalue()

HELP_TEXT = """
**How to Use This App:**

1. **Upload Data:**  
   Upload your CSV file with the sidebar uploader. You will see a preview and the shape of your data.

2. **Ask a Question or Give a Command:**  
   - *Analysis*: "Show average sales by region", "What is the top product?"
   - *Visualization*: "Plot sales over time", "Bar chart of layoffs by industry"
   - *Cleaning*: "Remove outliers from column X", "Fill missing values in age"
   - *Undo/Redo*: Use sidebar buttons if you need to revert a change.

3. **Review and Download:**
   - All generated code is shown for transparency.
   - Download your cleaned data and a full audit log at any time from the sidebar.

4. **AI Conversation Memory:**  
   The assistant remembers your previous questions, so you can ask follow-ups (e.g., "Now only for 2023", "Undo last cleaning").

**Notes:**
- *Support*: Only CSV files, up to 200MB.
- *Dependencies*: pandas, plotly, streamlit, langchain, Gemini/Google API key.
- *Contact*: See sidebar for developer details (Jinith Naik).

Enjoy smart, safe, and rapid data analytics! 🚀
"""

st.set_page_config(
    page_title="AI Data Analyst for all your analytics needs",
    layout="wide"
)

def main():
    st.markdown(
        "<h1 style='text-align: center; color: #0353A4;'>AI Data Analyst for all your analytics needs</h1>",
        unsafe_allow_html=True
    )
    st.caption("Built with Streamlit, LangChain, Gemini LLM, and 💙 for analytics.")

    initialize_states()

    with st.sidebar:
        st.header("🛠️ Workflow Controls")
        if st.button("⏪ Undo") and st.session_state.df_history:
            undo()
            st.success("Undo applied.")
        if st.button("⏩ Redo") and st.session_state.df_future:
            redo()
            st.success("Redo applied.")

        csv_buffer = io.StringIO()
        if st.session_state.df is not None:
            st.session_state.df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="⬇️ Download Cleaned Data",
                data=csv_buffer.getvalue(),
                file_name="ai_data_analyst_cleaned.csv",
                mime="text/csv"
            )
            st.download_button(
                label="⬇️ Download Audit Log",
                data=audit_log_csv(st.session_state.audit_log),
                file_name="ai_data_analyst_audit_log.csv",
                mime="text/csv"
            )
        if st.button("ℹ️ Help / Instructions"):
            st.session_state.show_help = True

        st.divider()
        st.subheader("About the Developer")
        st.markdown("""
**Jinith Naik**  
📱 +91 7990554873  
[LinkedIn](https://www.linkedin.com/in/jinithnaik/)  
[GitHub](https://github.com/Jinith-naik)  

Data Analyst & ML enthusiast | ISRO intern  
Python, SQL, Power BI, Tableau
        """)

        st.divider()
        st.subheader("Conversation History")
        history_text = st.session_state.memory.buffer or "No history yet."
        st.caption(history_text)

    if "show_help" in st.session_state and st.session_state.show_help:
        st.info(HELP_TEXT)
        if st.button("Close Help"):
            st.session_state.show_help = False

    with st.container():
        st.markdown("### 📥 Data Upload & Preview")
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
        if uploaded_file is not None:
            try:
                if st.session_state.df is None:
                    df = pd.read_csv(uploaded_file)
                    st.session_state.df = df
                    st.session_state.df_history = []
                    st.session_state.df_future = []
                    st.session_state.audit_log = []
                    st.success("CSV loaded.")
            except Exception as e:
                st.error(f"Error reading CSV file: {e}")
                return

        if st.session_state.df is not None:
            st.dataframe(st.session_state.df.head(), use_container_width=True)
            st.caption(f"Data shape: {st.session_state.df.shape}")
        else:
            st.info("Please upload a CSV file to continue.")

    st.markdown("---")
    st.markdown("### 💡 Ask, Clean, Analyze, or Visualize")

    if st.session_state.df is not None:
        llm = get_llm()
        question = st.text_area(
            "Ask a question, request a chart, or give a data cleaning instruction "
            "(e.g., 'Remove outliers', 'Show sales over time', 'Undo last cleaning'):",
            height=100
        )
        if question.strip():
            if st.button("Generate & Run", type="primary"):
                history = st.session_state.memory.buffer or ""
                with st.spinner("Generating code..."):
                    raw_code = generate_pandas_code(
                        llm, question, df=st.session_state.df, history=history)
                    cleaned_code = clean_code(raw_code)

                st.write("**Generated code:**")
                st.code(cleaned_code, language="python")

                local_env = {
                    'df': st.session_state.df.copy(),
                    'pd': pd,
                    'px': px
                }

                try:
                    exec(cleaned_code, {}, local_env)
                    modified_df = local_env.get('df')

                    if (modified_df is not None
                        and not modified_df.equals(st.session_state.df)):
                        push_to_history(st.session_state.df)
                        st.session_state.df = modified_df
                        st.success("DataFrame updated.")
                        log_audit(
                            st.session_state.audit_log, question, cleaned_code, "success",
                            "df modified"
                        )
                    else:
                        log_audit(
                            st.session_state.audit_log, question, cleaned_code, "success",
                            "no df modification"
                        )

                    fig = local_env.get('fig')
                    if fig:
                        with st.expander("Chart Output", expanded=True):
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        result = local_env.get('result')
                        if result is not None:
                            with st.expander("Query Output", expanded=True):
                                if isinstance(result, (pd.DataFrame, pd.Series)):
                                    st.dataframe(result)
                                else:
                                    st.write(result)
                        else:
                            dfs = [v for v in local_env.values() if isinstance(v, (pd.DataFrame, pd.Series))]
                            if dfs:
                                with st.expander("Output", expanded=True):
                                    st.dataframe(dfs[-1])
                            else:
                                st.info("No result or figure produced by the generated code.")

                    st.session_state.memory.save_context(
                        {"input": question}, {"output": cleaned_code}
                    )

                except Exception as e:
                    st.error(f"⚠️ Error executing generated code: {str(e)}")
                    log_audit(
                        st.session_state.audit_log, question, cleaned_code, "fail",
                        f"Error: {str(e)}"
                    )
        else:
            st.info("Enter your question, request, or cleaning instruction above to get started.")

    st.markdown(
        "<div style='text-align:center; color:gray; font-size:smaller;padding-top:16px;'>"
        "Made with ❤️ using Streamlit, LangChain, and Gemini LLM · &copy; 2025<br>"
        "Contact: Jinith Naik · +91 7990554873 · "
        "<a href='https://www.linkedin.com/in/jinithnaik/' target='_blank'>LinkedIn</a> · "
        "<a href='https://github.com/Jinith-naik' target='_blank'>GitHub</a>"
        "</div>", unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
