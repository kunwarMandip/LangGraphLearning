from IPython.display import Image, display
from app.task_1.graph_2 import first_graph



graph = first_graph()
try:
    # Save to file
    with open("graph.png", "wb") as f:
        f.write(graph.get_graph().draw_mermaid_png())

    print("Graph saved to graph.png")

    # Optionally open it (Windows only)

except Exception as e:
    print(f"Error generating graph: {e}")
