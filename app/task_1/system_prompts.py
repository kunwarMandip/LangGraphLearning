from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a project timeline manager."
     "Identify the task given by "
     "Break the task \"{task}\" into an Eisenhower matrix.")
])

def identify_query_system_prompt(user_prompt):
    SYSTEM_PROMPT = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a project timeline manager."
            "Identify the task in this given prompt \"{user_prompt}\"."
            "If the task is something that can be schedule"
            "Return a o"
        )
    ])
    return SYSTEM_PROMPT    

# def create_agent(system_prompt: str, user_prompt: str):
    