AI Data Analyst
🧠 A conversational, AI-powered data analytics and cleaning assistant. Visualize, transform, and explore your data with natural language — all in a modern Streamlit app.
🚀 Features

Conversational Data Analysis & Cleaning: Ask questions in plain English, and the assistant generates and executes pandas & Plotly code to analyze or clean your data.
Smart Visualizations: Request various charts and plots through natural language commands.
Versioning with Undo/Redo: Easily revert or reapply data cleaning or transformation steps.
Audit Logging: Every operation is logged with detailed info, enabling traceability and reproducibility.
Session State & Memory: The assistant remembers your previous queries and results for a coherent workflow.
Downloadable Cleaned Data & Logs: Export your current cleaned dataset and audit trail anytime.
Professional UI: Intuitive sidebar controls, conversation history, and help instructions included.

📦 Installation & Quickstart
Follow these steps to get the application running on your local machine.

Clone the Repository
git clone https://github.com/Jinith-naik/ai-data-analyst-app.git
cd ai-data-analyst-app


(Optional) Create & Activate a Virtual Environment
Linux/Mac:
python3 -m venv venv
source venv/bin/activate

Windows:
python -m venv venv
venv\Scripts\activate


Install Dependencies
pip install -r requirements.txt


Set Your Google Gemini API Key
Linux/Mac:
export GOOGLE_API_KEY="your-api-key-here"

Windows:
set GOOGLE_API_KEY="your-api-key-here"


Run the App
streamlit run main.py

Now, open your browser and navigate to http://localhost:8501.


📝 How to Use

Upload CSV File: Use the sidebar uploader to load your dataset.
Ask Questions: Type commands in the input box, such as:
"Show average sales by region"
"Remove duplicates"
"Fill missing values in the 'age' column with the mean"
"Plot a bar chart of layoffs by location"


Undo/Redo: Use the buttons to revert or reapply changes to your data.
History: The sidebar shows the full conversation history with the assistant.
Download: The cleaned dataset and audit logs are available for download at any time.

🧩 Tech Stack

Streamlit: UI & web app framework
LangChain + Gemini LLM: Natural language understanding & memory
Pandas & Plotly: Data wrangling and visualizations

🛡️ Security & Privacy

Your dataset is processed locally; only the text from your prompts is sent to the Gemini LLM.
API keys are handled securely as environment variables and are not committed to the repository.
Always follow your organization’s data privacy policies when handling sensitive data.

👤 About The Developer
Jinith Naik | Data Analyst & Machine Learning Enthusiast

Phone: +91 7990554873
LinkedIn: linkedin.com/in/jinith-naik
GitHub: github.com/Jinith-naik
Skills: Python, SQL, Power BI, Tableau, AI Workflows

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to fork the repository and create a pull request.
📄 License
This project is licensed under the MIT License.
