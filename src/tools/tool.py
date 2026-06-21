from langchain_community.tools.github.tool import GitHubAction
from langchain_community.utilities.github import GitHubAPIWrapper
import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from typing import List,Any,Optional,Dict,Annotated,Type
from pydantic import BaseModel, Field

load_dotenv(override=True)


github_wrapper = GitHubAPIWrapper(
    github_app_private_key = os.getenv("APP_PRIVATE_KEY"),
    github_app_id = int(os.getenv("APP_ID")),
    github_repository = os.getenv('REPOSITORY'),
)

class githubinput(BaseModel):
    instructions: str = Field(default="", description="GitHub operation instructions")

class GitHub(BaseTool):
    """Tool for interacting with github api """
    api_wrapper:Any
    mode:str="get_pull_requests"
    name: str="list_open_pull_requests"
    description :str =  "Tool for interacting with github repository PR"
    args_schema : Optional[Type[BaseModel]] = githubinput



    def _run(self,instructions: Optional[str]=" ",run_manager : Optional[CallbackManagerForToolRun] = None,**kwargs:Any,) ->str :
        """ use the github api to run the operations"""
        if not instructions or instructions =={}:
            #catch any other form of input from LLM
            instructions = " "
        
        return self.api_wrapper.run(self.mode,instructions)



github_tool = GitHub(
    api_wrapper=github_wrapper,
    mode="list_open_pull_requests"
)

