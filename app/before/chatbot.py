from app.main import stream_graph_updates

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break