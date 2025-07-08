# from app.task_1.llm_info import llm
# from app.task_1.states import MyState, TaskState
# from langgraph.graph import StateGraph, START, END
# from langgraph.checkpoint.memory import MemorySaver
# from langchain_core.prompts import ChatPromptTemplate
# import json
# from datetime import datetime

# from typing_extensions import TypedDict, List
# tasks: List[TaskState] = []

# def identify_query(state: dict) -> dict:
#     SYSTEM_PROMPT = {
#         "role": "system",
#         "content": (
#             "You are a helpful assistant. "
#             "Return True if the user’s prompt is a schedulable task, "
#             "otherwise return False."
#         )
#     }
#     # Ask the LLM and store the answer
#     state["is_task"] = bool(llm.invoke([SYSTEM_PROMPT, *state["messages"]]))
#     print(state["is_task"])
#     return state


# def identify_task(state: MyState):
#     SYSTEM_PROMPT = {
#         "role": "system",
#         "content": (
#             "You are a helpful assistant that identifies and categorizes tasks. "
#             "Analyze the user's request and extract the main task information. "
#             "Determine the priority using the Eisenhower Matrix: "
#             "1 = Urgent & Important, 2 = Urgent & Not Important, "
#             "3 = Important & Not Urgent, 4 = Not Important & Not Urgent (Ignorable). "
#             "Respond ONLY with valid JSON in this format:\n"
#             "{\n"
#             '  "goal": "string description of the task",\n'
#             '  "priority": 1,\n'
#             '  "deadline": "2024-12-31T23:59:59" (optional)\n'
#             "}\n"
#             "Example:\n"
#             "{\n"
#             '  "goal": "Complete project proposal",\n'
#             '  "priority": 1,\n'
#             '  "deadline": "2024-12-31T23:59:59"\n'
#             "}"
#         )
#     }
    
#     messages = [SYSTEM_PROMPT, *state["messages"]]
#     reply = llm.invoke(messages)

    
#     try:
#         json_response = json.loads(reply.content)
#         task_id = add_tasks(json_response, state)  # Returns the task ID
#         print(json_response)
#         print(f"Added task with ID: {task_id}")
#         return {"messages": state["messages"] + [reply], "task_id": task_id}
#     except (json.JSONDecodeError, KeyError, ValueError) as e:
#         print(f"Error parsing JSON response: {e}")
#         print("Raw response:", reply.content)
#         return {"messages": state["messages"] + [reply], "task_state": None}
    
#     return {"messages": state["messages"] + [reply]} 

# def add_task(json_data, state):
#     """Add a new task and return its index/ID"""
#     new_task = TaskState(**json_data)
#     tasks.append(new_task)
#     return len(tasks) - 1  # Return the index as task ID

# def add_tasks(jsonFile, state):
#     tasks.append(TaskState(**jsonFile))
    

# def identify_subtasks(state: MyState):
#     print("hello world")
#     latest_message = state["messages"][-1].content  # Access the last message in the list
#     # print(latest_message['content'])
#     print(latest_message)

    
#     chat_prompt = ChatPromptTemplate.from_messages([
#         ("system", """You are a helpful assistant that identifies and categorizes tasks. 
#             Take the user json and extract the task information. 
#             Break the task into a subset of small goals that can be taken to achieve this.
#             Determine the priority of each subset of task using the Eisenhower Matrix: 
#             1 = Urgent & Important, 2 = Urgent & Not Important, 
#             3 = Important & Not Urgent, 4 = Not Important & Not Urgent (Ignorable). 
#             For tasks that require a deadline, ensure the date is in the format: 
#             YYYY-MM-DDTHH:MM:SS
#             "Respond ONLY with valid JSON in this format:\n":
#             {{
#                 "description": "string description of the task",
#                 "priority": 1,
#                 "completed": false,
#                 "deadline": "2024-12-31T23:59:59" (optional)
#             }}
#             """),
#         ("human", "{latest_message}")
#     ])
    
#     formatted_messages = chat_prompt.format_messages(latest_message=latest_message)
#     reply = llm.invoke(formatted_messages)
#     try:
#         json_response = json.loads(reply.content)
#         add_tasks(json_response, state)
#         print(json_response)
#         print(tasks)
#     except (json.JSONDecodeError, KeyError, ValueError) as e:
#         print(f"Error parsing JSON response: {e}")
#         print("Raw response:", reply.content)
#         return {"messages": state["messages"] + [reply], "task_state": None}
    
#     return {"messages": state["messages"] + [reply]} 



# def verify_both(state: MyState):
#     return "verifying both"



# def get_query(state: MyState):
#     return "query on that day"


# def first_graph():
#     memory = MemorySaver()
#     graph_builder = StateGraph(MyState)
    
#     #Create nodes
#     graph_builder.add_node("identify_query", identify_query)
#     graph_builder.add_node("identify_task", identify_task)
#     graph_builder.add_node("identify_subtasks", identify_subtasks)
#     # graph_builder.add_node("verify_both", verify_both)
#     graph_builder.add_node("get_query", get_query)

#     #Set START and END edge
#     graph_builder.add_edge(START, "identify_query")
#     graph_builder.add_edge("identify_subtasks", END)
#     graph_builder.add_edge("get_query", END)

#     # Create conditional edges
#     graph_builder.add_conditional_edges(
#         "identify_query",
#         lambda s: s["is_task"],      # <- this tiny lambda replaces route_after_identify
#         {
#             True:  "identify_task",  # follow this edge if the prompt *is* a task
#             False: END               # otherwise end the graph
#         }
#     )
    
#     #Mandatory edges
#     graph_builder.add_edge("identify_task", "identify_subtasks")
#     # graph_builder.add_edge("identify_subtasks", "verify_both")
#     graph = graph_builder.compile(checkpointer=memory)

#     return graph 


    
from app.task_1.llm_info import llm
from app.task_1.states import MyState, TaskState, SubTask
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate
import json
from datetime import datetime

from typing_extensions import TypedDict, List
tasks: List[TaskState] = []

def identify_query(state: dict) -> dict:
    SYSTEM_PROMPT = {
        "role": "system",
        "content": (
            "You are a helpful assistant. "
            "Return True if the user's prompt is a schedulable task, "
            "otherwise return False."
        )
    }
    # Ask the LLM and store the answer
    state["is_task"] = bool(llm.invoke([SYSTEM_PROMPT, *state["messages"]]))
    print(state["is_task"])
    return state


def identify_task(state: MyState):
    SYSTEM_PROMPT = {
        "role": "system",
        "content": (
            "You are a helpful assistant that identifies and categorizes tasks. "
            "Analyze the user's request and extract the main task information. "
            "Determine the priority using the Eisenhower Matrix: "
            "1 = Urgent & Important, 2 = Urgent & Not Important, "
            "3 = Important & Not Urgent, 4 = Not Important & Not Urgent (Ignorable). "
            "Respond ONLY with valid JSON in this format:\n"
            "{\n"
            '  "goal": "string description of the task",\n'
            '  "priority": 1,\n'
            '  "deadline": "2024-12-31T23:59:59" (optional)\n'
            "}\n"
            "Example:\n"
            "{\n"
            '  "goal": "Complete project proposal",\n'
            '  "priority": 1,\n'
            '  "deadline": "2024-12-31T23:59:59"\n'
            "}"
        )
    }
    
    messages = [SYSTEM_PROMPT, *state["messages"]]
    reply = llm.invoke(messages)

    
    try:
        json_response = json.loads(reply.content)
        task_id = add_task(json_response, state)  # Fixed function name
        print(json_response)
        print(f"Added task with ID: {task_id}")
        return {"messages": state["messages"] + [reply], "task_id": task_id}
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error parsing JSON response: {e}")
        print("Raw response:", reply.content)
        return {"messages": state["messages"] + [reply], "task_state": None}
    
    return {"messages": state["messages"] + [reply]} 

def add_task(json_data, state):
    """Add a new task and return its index/ID"""
    new_task = TaskState(**json_data)
    tasks.append(new_task)
    return len(tasks) - 1  # Return the index as task ID

def add_subtask_to_task(task_id: int, subtask_data: dict):
    """Add a subtask to an existing task"""
    if 0 <= task_id < len(tasks):
        new_subtask = SubTask(**subtask_data)
        tasks[task_id].subtasks.append(new_subtask)
        return True
    return False

def identify_subtasks(state: MyState):
    print("hello world")
    latest_message = state["messages"][-1].content  # Access the last message in the list
    print(latest_message)

    # Get the task_id from the state
    task_id = state.get("task_id", None)
    if task_id is None:
        print("No task_id found in state")
        return {"messages": state["messages"], "task_state": None}
    
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant that identifies and categorizes tasks. 
            Take the user json and extract the task information. 
            Break the task into a list of small subtasks that can be taken to achieve this.
            Determine the priority of each subtask using the Eisenhower Matrix: 
            1 = Urgent & Important, 2 = Urgent & Not Important, 
            3 = Important & Not Urgent, 4 = Not Important & Not Urgent (Ignorable). 
            For tasks that require a deadline, ensure the date is in the format: 
            YYYY-MM-DDTHH:MM:SS
            "Respond ONLY with valid JSON in this format (array of subtasks):\n":
            [
                {{
                    "description": "string description of the subtask",
                    "priority": 1,
                    "completed": false,
                    "deadline": "2024-12-31T23:59:59" (optional)
                }},
                {{
                    "description": "string description of another subtask",
                    "priority": 2,
                    "completed": false,
                    "deadline": "2024-12-31T23:59:59" (optional)
                }}
            ]
            """),
        ("human", "{latest_message}")
    ])
    
    formatted_messages = chat_prompt.format_messages(latest_message=latest_message)
    reply = llm.invoke(formatted_messages)
    
    try:
        json_response = json.loads(reply.content)
        
        # Handle both single subtask and array of subtasks
        if isinstance(json_response, dict):
            # Single subtask
            success = add_subtask_to_task(task_id, json_response)
            if success:
                print(f"Added subtask to task {task_id}: {json_response}")
            else:
                print(f"Failed to add subtask to task {task_id}")
        elif isinstance(json_response, list):
            # Multiple subtasks
            for subtask_data in json_response:
                success = add_subtask_to_task(task_id, subtask_data)
                if success:
                    print(f"Added subtask to task {task_id}: {subtask_data}")
                else:
                    print(f"Failed to add subtask to task {task_id}")
        
        print("Current tasks with subtasks:")
        for i, task in enumerate(tasks):
            print(f"Task {i}: {task.goal}")
            for j, subtask in enumerate(task.subtasks):
                print(f"  Subtask {j}: {subtask.description}")
                
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error parsing JSON response: {e}")
        print("Raw response:", reply.content)
        return {"messages": state["messages"] + [reply], "task_state": None}
    
    return {"messages": state["messages"] + [reply]} 

def verify_both(state: MyState):
    return "verifying both"

def get_query(state: MyState):
    return "query on that day"

def first_graph():
    memory = MemorySaver()
    graph_builder = StateGraph(MyState)
    
    #Create nodes
    graph_builder.add_node("identify_query", identify_query)
    graph_builder.add_node("identify_task", identify_task)
    graph_builder.add_node("identify_subtasks", identify_subtasks)
    # graph_builder.add_node("verify_both", verify_both)
    graph_builder.add_node("get_query", get_query)

    #Set START and END edge
    graph_builder.add_edge(START, "identify_query")
    graph_builder.add_edge("identify_subtasks", END)
    graph_builder.add_edge("get_query", END)

    # Create conditional edges
    graph_builder.add_conditional_edges(
        "identify_query",
        lambda s: s["is_task"],      # <- this tiny lambda replaces route_after_identify
        {
            True:  "identify_task",  # follow this edge if the prompt *is* a task
            False: END               # otherwise end the graph
        }
    )
    
    #Mandatory edges
    graph_builder.add_edge("identify_task", "identify_subtasks")
    # graph_builder.add_edge("identify_subtasks", "verify_both")
    graph = graph_builder.compile(checkpointer=memory)

    return graph