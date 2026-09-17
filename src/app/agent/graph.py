from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# [NEW]: Naya SQL tool import karo
from app.agent.tools import execute_sql_query

load_dotenv()

# 1. LLM Model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

# 2. Tools
tools = [execute_sql_query]

# 3. System Prompt with Database Schema
system_prompt = """
You are RepoPilot, an AI software engineering assistant.
You help users inspect and analyze their synchronized GitHub repositories.
Always use the `execute_sql_query` tool to answer questions by running SQL SELECT queries against the local PostgreSQL database.

Database Schema:
Table: repositories
Columns:
  - id (integer)
  - github_id (integer)
  - name (varchar)
  - full_name (varchar)
  - owner (varchar)
  - description (text)
  - private (boolean)
  - html_url (varchar)
  - default_branch (varchar)
  - language (varchar)
  - created_at (timestamp)
  - updated_at (timestamp)
  - pushed_at (timestamp)

Rules:
1. To count repositories, ALWAYS use: SELECT COUNT(*) FROM repositories;
2. To filter by language, use: WHERE language = '...'
3. To find inactive repos: WHERE pushed_at < NOW() - INTERVAL '6 months'
4. Only write read-only SELECT queries.
"""

# 4. In-Context Memory Checkpointer
checkpointer = MemorySaver()

# 5. Agent
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=system_prompt,
    checkpointer=checkpointer,
)