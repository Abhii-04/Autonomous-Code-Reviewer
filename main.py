import argparse
from dotenv import load_dotenv
from src.agent import run_agent

DEFAULT_TASK = "Check if there is any PR on the current repository."

def main():
    load_dotenv(override=True)
    
    parser = argparse.ArgumentParser(description="Run the GitHub PR review agent.")
    parser.add_argument("task", nargs="*", help="Task for the agent to perform")
    args = parser.parse_args()
    
    task = " ".join(args.task) or DEFAULT_TASK
    print(run_agent(task)["messages"][-1].content)

if __name__ == "__main__":
    main()