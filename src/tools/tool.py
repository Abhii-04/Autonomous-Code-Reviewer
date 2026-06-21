from langchain_community.utilities.github import GitHubAPIWrapper
import os
from dotenv import load_dotenv
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from typing import Any,Optional,Type
from pydantic import BaseModel, Field

load_dotenv(override=True)


def _env(*names: str) -> Optional[str]:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


def create_github_wrapper() -> GitHubAPIWrapper:
    github_app_id = _env("GITHUB_APP_ID", "APP_ID")
    github_app_private_key = _env("GITHUB_APP_PRIVATE_KEY", "APP_PRIVATE_KEY")
    github_repository = _env("GITHUB_REPOSITORY", "REPOSITORY")

    missing = [
        name
        for name, value in {
            "GITHUB_APP_ID": github_app_id,
            "GITHUB_APP_PRIVATE_KEY": github_app_private_key,
            "GITHUB_REPOSITORY": github_repository,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing required GitHub configuration: {', '.join(missing)}")

    return GitHubAPIWrapper(
        github_app_private_key=github_app_private_key,
        github_app_id=github_app_id,
        github_repository=github_repository,
    )

class githubinput(BaseModel):
    instructions: str = Field(default="", description="GitHub operation instructions")

class GitHub(BaseTool):
    """Tool for interacting with github api """
    api_wrapper:Optional[Any] = None
    mode:str="get_pull_requests"
    name: str="list_open_pull_requests"
    description :str =  "Tool for interacting with github repository PR"
    args_schema : Optional[Type[BaseModel]] = githubinput



    def _run(self,instructions: Optional[str]=" ",run_manager : Optional[CallbackManagerForToolRun] = None,**kwargs:Any,) ->str :
        """ use the github api to run the operations"""
        if not instructions or instructions =={}:
            #catch any other form of input from LLM
            instructions = " "
        
        api_wrapper = self.api_wrapper or create_github_wrapper()
        return api_wrapper.run(self.mode,instructions)



github_tool = GitHub(
    mode="list_open_pull_requests"
)
