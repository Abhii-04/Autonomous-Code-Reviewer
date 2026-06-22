from langchain_task_steering import TaskSteeringMiddleware, Task



task_steering_pipeline = TaskSteeringMiddleware(
    tasks=[
        Task(
            name="collect",
            instruction="Collect all relevant items from the user's input.",
            tools=[],
        ),
        Task(
            name="categorize",
            instruction="Organize the collected items into categories.",
            tools=[],
        ),
    ],
)