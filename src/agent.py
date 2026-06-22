from platform import architecture
from src.tools.tool import github_tool
from src.prompt import github_agent_prompt, orchestrator_prompt,security_agent_prompt,style_agent_prompt,tests_agent_prompt,architecture_agent_prompt
import os 
from dotenv import load_dotenv
from deepagents import create_deep_agent , FilesystemPermission, create_deep_agent
from langchain_openai import ChatOpenAI
from pathlib import Path
from typing import Any,Annotated,List,Dict
from deepagents.backends.filesystem import FilesystemBackend

load_dotenv(override=True)
PROJECT_ROOT = Path(__file__).resolve().parents[1]


llm = ChatOpenAI(
    api_key = ${{ secrets.DEEPSEEK_API_KEY }},
    model = 'deepseek-v4-flash',
    base_url = "https://api.deepseek.com"
)

tools = [github_tool]
git_tool = [github_tool]
security_tools = []
architecture_tools = []
style_tool = []
test_tool = []

def orchestrator():
    
    return create_deep_agent(
        model = llm,
        tools = tools ,
        system_prompt=orchestrator_prompt,
        skills = ["/skills"],
        memory = ["memory/"],
        backend=FilesystemBackend(root_dir = PROJECT_ROOT),
        permissions=FilesystemPermission(
            operations= ["read","write"],
            paths = ["/reports/"],
            mode="allow",
        ),
        subagents = [
            {
                "name" : "security_checker",
                "description": "Use this to check if code is secure or not",
                "system_prompt": security_agent_prompt,
                "tools" : security_tools
            },
            {
                "name": "style_agent",
                "description": "Use this agent to check the design and stype of the PR ",
                "system_prompt":style_agent_prompt,
                "tools":style_tool,
            },
            {
                "name":"test_agent",
                "description":"Use this agent to test the product whether it is working or not",
                "system_prompt":tests_agent_prompt,
                "tools":test_tool,
            },
            {
                "name":"architecture_agent",
                "description": "Use this agent to check the architecture of the code ",
                "system_prompt": architecture_agent_prompt,
                "tools":architecture_tools,
            },
            {
                "name": "github_agent",
                "description": "Use this agent to interact with github",
                "system_prompt":github_agent_prompt,
                "tools": git_tool,
            }

        ],
    )




def run_agent(task: str) -> Any:
    agent = orchestrator()
    return agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": task,
            }
        ]
    })
