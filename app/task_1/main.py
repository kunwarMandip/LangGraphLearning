from app.task_1.llm_info import llm
from app.task_1.graph import step_1
from app.task_1.graph_2 import first_graph


config = {
    "configurable": {
        "thread_id": "chat_thread"
    }
}

input_1 = {
    "messages": [
        {"role": "user", "content": "Who is the prime minister of UK?"}
    ]
}


input_2 = {
    "messages": [
        {"role": "user", "content": "Set me a time to play football for 2pm tomorrow"}
    ]
}


input_3 = {
    "messages": [
        {"role": "user", "content": "What were my previous prompts?"}
    ]
}

graph = first_graph()

results = graph.invoke(input_2, config= config)
print(results)
# print(results)

# results = graph.invoke(input_2, config= config)
# print(results)

# results = graph.invoke(input_3, config= config)
# print(results)