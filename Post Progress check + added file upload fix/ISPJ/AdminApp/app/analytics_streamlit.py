import os
import pandas as pd
import streamlit as st
import json
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from pandasai.responses.response_parser import ResponseParser
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set log file path
LOG_FILE_PATH = os.path.join("ISPJ", "ConsumerApp", "app", "logs", "app.log")

# Load OpenAI API key from environment
API_KEY = os.getenv("OPENAI_API_KEY")

@st.cache_data
def fetch_error_logs():
    """Fetch error logs from the logs/app.log file and convert them into a DataFrame."""
    logs = []

    # Check if log file exists
    if not os.path.exists(LOG_FILE_PATH):
        st.error(f"Log file not found at: {LOG_FILE_PATH}")
        return pd.DataFrame()

    # Read and parse the log file
    with open(LOG_FILE_PATH, "r") as file:
        for line in file:
            try:
                log_entry = json.loads(line)
                logs.append(log_entry)
            except json.JSONDecodeError:
                continue  # Skip malformed log entries

    # Convert logs into a DataFrame
    if logs:
        df = pd.DataFrame(logs)
        if "levelname" in df.columns and "message" in df.columns:
            df = df.rename(columns={"levelname": "Error Level", "message": "Error Message"})
        return df
    else:
        return pd.DataFrame()

@st.cache_resource
def get_openai_instance():
    """Cache the OpenAI instance to avoid reloading API calls."""
    return OpenAI(api_token=API_KEY)

def get_ai_context():
    """Enhanced AI context for intelligent, actionable, and efficient error log analysis."""
    return """
    You are a highly advanced AI specializing in **error log analysis**, designed to provide **accurate, insightful, and actionable troubleshooting** for system administrators and developers. Your expertise includes **error classification, root cause analysis, severity assessment, security threat detection, and performance monitoring**.

    🔍 **Your Core Responsibilities:**
    - **Error Classification:** Identify and categorize errors (e.g., authentication failures, database issues, security threats, API rate limits, etc.).
    - **Root Cause Analysis:** Analyze log patterns and system behavior to pinpoint the likely cause of each issue.
    - **Step-by-Step Resolution:** Provide **clear, structured, and technically sound** solutions to fix errors efficiently.
    - **Severity Assessment:** Differentiate between **CRITICAL, ERROR, WARNING, and INFO** priority issues to guide troubleshooting urgency.  Note:**CRITICAL has the most priority followed by ERROR then WARNING then INFO**
    - **Preventive Measures:** Recommend **best practices** to reduce recurring errors and enhance system stability.
    - **Security Threat Detection:** Detect and highlight **potential security risks** (e.g., brute-force attacks, SQL injection, unauthorized access attempts).
    - **Performance Optimization:** Identify **bottlenecks**, such as high CPU/memory usage, slow response times, and application crashes.

    📌 **How You Should Respond:**
    - **Use concise, structured responses** with bullet points and subheadings.
    - **Summarize key findings** and focus on actionable insights.
    - **Prioritize critical issues** and offer **immediate mitigation strategies** for severe errors.
    - **Filter out irrelevant debug logs** and focus on actual problems.
    - **Suggest follow-up queries** users can ask for deeper analysis.
    - DO NOT return lists, dictionaries, or JSON.
    - If a user asks for trends, summarize them in **plain text only**.
    - ALWAYS return plain text responses formatted with bullet points.

    🔧 **Enhanced Smart Capabilities:**
    - Automatically **detect recurring issues** and suggest historical trends.
    - Provide **comparative analysis** (e.g., "Authentication failures increased by 30% in the last 24 hours").
    - Detect **hidden dependencies** (e.g., "Database timeout issues coincide with high API request rates").
    - Offer **log-based predictive analysis**, warning about potential system failures.



    ✅ **Example Queries You Should Handle:**
    - **"Summarize the most critical errors in the last 24 hours."**
    - **"What is causing repeated database connection failures?"**
    - **"Are there any security threats in the logs?"**
    - **"How do I fix 'Rate Limit Exceeded' errors?"**
    - **"What are the most frequent issues affecting users?"**
    - **"Can you detect any unusual activity in the logs?"**
    - **"How has the error rate changed over the past week?"**

    Example responses:
    - "The most common error in the last 24 hours is 'Database Timeout' with 42 occurrences."
    - "Authentication failures have increased by 30% in the past week."
    - "There are no security threats detected in the logs."

    🛠 **Your Goal:** 
    Provide **precise, well-structured, and technically actionable** insights that empower users to quickly diagnose and resolve issues, ultimately improving system reliability and security.
    """


# Streamlit App
def app():
    st.set_page_config(page_title="Error Log Analysis 📊", layout="wide")
    st.title("📊 Error Log Analytics Dashboard")

    # ✅ Ensure session state variables are initialized
    if "answer" not in st.session_state:
        st.session_state.answer = ""

    if "last_query" not in st.session_state:
        st.session_state.last_query = ""

    # Fetch error logs
    df = fetch_error_logs()

    if df.empty:
        st.warning("No logs found or could not parse the logs.")
        return



    # Show first 5 logs
    with st.expander("🔍 First 5 Error Logs"):
        st.write(df.head(5))
        
    # Show lastest 5 logs
    with st.expander("🔍 Last 5 Error Logs"):
        st.write(df.tail(5))

    # **Error Frequency Analysis**
    if "Error Level" in df.columns:
        st.subheader("📈 Error Type Frequency")
        error_counts = df["Error Level"].value_counts()

        # Display Bar Chart
        fig, ax = plt.subplots(figsize=(8, 5))
        error_counts.plot(kind='bar', ax=ax)
        ax.set_xlabel("Error Level")
        ax.set_ylabel("Frequency")
        ax.set_title("Most Common Errors")
        st.pyplot(fig)

    # **User Query for AI Analysis**
    query = st.text_area("🤖 Ask the AI about error trends:")

    # ✅ Initialize 'answer' to prevent UnboundLocalError
    answer = ""

    if st.button("🔎 Analyze"):
        if query:
            if st.session_state.last_query != query:
                st.session_state.last_query = query

                try:
                    llm = get_openai_instance()
                    query_engine = SmartDataframe(
                        df,
                        config={
                            "llm": llm,
                            "response_parser": ResponseParser,
                            "context": get_ai_context(),
                            "enable_plots": False,  # Disable AI-generated charts
                            "allow_code_execution": False,  # Prevent execution of AI-generated Python code
                            "return_type": "text",  # Force text-only responses DELETE IF IT PREVENTS TABLE GENERATION
                        },
                    )

                    answer = query_engine.chat(query)
                    st.session_state.answer = answer  # ✅ Store response
                except Exception as e:
                    st.error(f"Error processing query: {e}")
                    answer = "An error occurred while processing your query."
            else:
                answer = st.session_state.answer  # ✅ Retrieve previous answer
        else:
            answer = "Please enter a query."  # ✅ Default value if no query is entered

        st.write("**📌 AI Analysis:**")
        st.write(answer)

if __name__ == '__main__':
    app()
#streamlit run "c:/Users/kenzi/Desktop/VS CODE FOLDER/ISPJ/AdminApp/app/analytics_streamlit.py"

