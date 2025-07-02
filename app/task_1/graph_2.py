from app.task_1.llm_info import llm
from app.task_1.states import MyState
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a project timeline manager."
     "Identify the task given by "
     "Break the task \"{task}\" into an Eisenhower matrix.")
])

def identify_query(state: MyState):
    return True

def should_end(state: MyState):
    return False

def identify_task(state: MyState):
    return "identify tasks"

def identify_subtasks(state: MyState):
    return "identify subtasks"

def verify_task(state: MyState):
    return "verifying tasks"

def verify_subtasks(state: MyState):
    return "verifying sub tasks"

def verify_both(state: MyState):
    return "verifying both"

def add_task(state: MyState):
    return "adding tasks"
    
def add_subtasks(state: MyState):
    return "adding sub_tasks"

def get_query(state: MyState):
    return "query on that day"


def first_graph():
    memory = MemorySaver()
    graph_builder = StateGraph(MyState)
    #Create nodes
    graph_builder.add_node("identify_query", identify_query)
    graph_builder.add_node("identify_task", identify_task)
    graph_builder.add_node("identify_subtasks", identify_subtasks)
    graph_builder.add_node("verify_task", verify_task)
    graph_builder.add_node("verify_subtasks", verify_subtasks)
    graph_builder.add_node("verify_both", verify_both)
    graph_builder.add_node("add_task", add_task)
    graph_builder.add_node("add_subtasks", add_subtasks)
    graph_builder.add_node("get_query", get_query)

    #Set START and END edge
    graph_builder.add_edge(START, "identify_query")
    graph_builder.add_edge("verify_both", END)
    graph_builder.add_edge("get_query", END)

    #Create conditional edges
    graph_builder.add_conditional_edges(
        "identify_query",
        should_end,
        {
            True: "identify_task",
            False: "get_query"              
        }
    )

    
    #Mandatory edge checks direction
    graph_builder.add_edge("identify_task", "verify_task")
    graph_builder.add_edge("verify_task", "add_task")
    graph_builder.add_edge("add_task", "identify_subtasks")
    graph_builder.add_edge("identify_subtasks", "verify_subtasks")
    graph_builder.add_edge("verify_subtasks", "add_subtasks")
    graph_builder.add_edge("add_subtasks", "verify_both")

    graph = graph_builder.compile(checkpointer=memory)

    return graph 


