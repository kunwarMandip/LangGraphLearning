from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt.chat_agent_executor import AgentState
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
#     task_message = f"Divide the task into "
#     system_message = f"You are a helpful assistant. Address the user as"
#     return [
#         {"role": "system", "content": system_message + state["messages"]}
#     ]


helpful_assistant = f"System", "You are a helpful assistant. Complete the user prompt step by step."

task_break_down_prompt = ChatPromptTemplate.from_messages([
    (   
        helpful_assistant+
        f"Identify the task given by the user. " +
        f"Break down the task into sub parts so that i cant be tackled easily. " +
        f"For example, a report could be broken down into writing introduction, verifying data, creating a conclusion and formatting a report."
    ),
    (MessagesPlaceholder("messages")),
])


###STEP 2: Subtask Categorization###
# sub_task_categorization = (
#     helpful_assistant +
#     f""
# )