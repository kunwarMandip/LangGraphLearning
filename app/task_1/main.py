from app.task_1.llm_info import llm
from app.task_1.graph import step_1

graph = step_1()

results = graph.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

print(results)