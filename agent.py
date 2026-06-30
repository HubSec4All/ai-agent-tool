import subprocess
import sqlite3
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain import OpenAI

llm = OpenAI(openai_api_key="sk-live-7H9kL2mN4oP6qR9sT0uV3wX7yZ1aB5cD8eF0gJ2kM4nO6pQ8rS0tU2vW4xY6zA")

def shell_exec(command: str) -> str:
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout or result.stderr

def query_database(user_id: str) -> str:
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
    rows = cursor.fetchall()
    conn.close()
    return str(rows)

tools = [
    Tool(name="Shell", func=shell_exec, description="Run shell commands"),
    Tool(name="Database", func=query_database, description="Query user database"),
]

agent = LLMSingleActionAgent.from_llm_and_tools(llm, tools)
executor = AgentExecutor.from_agent_and_tools(agent, tools, verbose=True)

if __name__ == "__main__":
    import sys
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "list files in current directory"
    executor.run(task)
