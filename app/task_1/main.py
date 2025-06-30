from app.task_1.llm_info import llm
from app.task_1.graph import step_1


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
        {"role": "user", "content": "What is a dog?"}
    ]
}


input_3 = {
    "messages": [
        {"role": "user", "content": "What were my previous prompts?"}
    ]
}

graph = step_1()

results = graph.invoke(input_1, config= config)
print(results)

results = graph.invoke(input_2, config= config)
print(results)

results = graph.invoke(input_3, config= config)
print(results)