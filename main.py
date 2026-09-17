from dotenv import load_dotenv

from core.flow import Flow
from nodes import LoaderNode, ExecNode, LLMNode

load_dotenv()

if __name__ == "__main__":
    flow = Flow("Validator")
    flow.add_node(LoaderNode("LoaderNode"), is_start=True)
    flow.add_node(ExecNode("ExecNode"))
    flow.add_node(LLMNode("LLMNode"))

    flow.state.set("problem_name", "two_sum")
    flow.state.set("solution_path", "problems/two_sum/solution.py")
    flow.run()