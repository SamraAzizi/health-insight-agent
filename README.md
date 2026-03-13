## Overviews
HIA (Health Insights Agent)

AI Agent to analyze blood reports and provide detailed health insights.

## features
- Agent-based architecture
    - Analysis Agent: Report analysis with in-context learning from  - - previous analyses and a built-in knowledge base
Chat Agent: RAG-powered follow-up Q&A over your report (FAISS + HuggingFace embeddings)
- Multi-model cascade via Groq with automatic fallback (primary → secondary → tertiary → fallback)
- Chat sessions: Create multiple analysis sessions; each session stores report, analysis, and follow-up messages in Supabase
- Report sources: Upload your own PDF or use the built-in sample report for quick testing
- PDF handling: Upload up to 20MB, max 50 pages; validation for file type and medical-report content
- Daily analysis limit: Configurable cap (default 15/day) with countdown in the sidebar
- Secure auth: Supabase Auth (sign up / sign in), session validation, and configurable session timeout
- Session history: View, switch, and delete past sessions; report text persisted for follow-up chat across reloads
- Modern UI: Responsive Streamlit app with sidebar session list, user greeting, and real-time feedback

## Tech Stack

- Frontend: Streamlit (1.42+)
- AI / LLM
    - Report analysis: Groq with multi-model fallback via ModelManager
        - Primary: meta-llama/llama-4-maverick-17b-128e-instruct
        - Secondary: llama-3.3-70b-versatile
        - Tertiary: llama-3.1-8b-instant
        - Fallback: llama3-70b-8192
    - Follow-up chat: RAG with LangChain, HuggingFace embeddings (all-MiniLM-L6-v2), FAISS vector store, and Groq (llama-3.3-70b-versatile)
- Database: Supabase (PostgreSQL)
    - Tables: users, chat_sessions, chat_messages
- Auth: Supabase Auth, Gotrue
- PDF: PDFPlumber (text extraction), filetype (file validation)
- Libraries: LangChain, LangChain Community, LangChain HuggingFace, LangChain Text Splitters, sentence-transformers, FAISS (CPU)

## Installation
Requirements

- Python 3.8+
- Streamlit 1.42+
- Supabase account
- Groq API key
- PDFPlumber, filetype

Getting Started
1. Clone the repository:
```bash
git clone https://github.com/SamraAzizi/health-insight-agent.git
cd hia
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Required environment variables(in `..streamlit/secrets.toml`)
```bash
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-key"
GROQ_API_KEY = "your-groq-api-key"
```
4. Set up Supbase database schemas;
The application uses three tables: `users`, `chat_sessions`, and `chat_messages`. Use the SQL script at `public/db/script.sql` to create them.

5. Run the application:
```bash
streamlit run src\main.py
```