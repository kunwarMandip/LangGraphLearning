from IPython.display import Image, display
from app.task_1.graph_visual import graph_builder as graph

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass