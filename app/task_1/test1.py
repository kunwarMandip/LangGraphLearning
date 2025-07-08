# pretend these are your previous chat turns
state = {"messages": ["User: Hi", "Assistant: Hello again"]}

system_msg = "System: Follow the rules"

# 1) WITHOUT the *  ──> keeps a nested list
messages_nested = [system_msg, state["messages"]]

# 2) WITH the *     ──> unpacks (flattens) the list
messages_flat   = [system_msg, *state["messages"]]

print("messages_nested =", messages_nested)
print("messages_flat   =", messages_flat)
