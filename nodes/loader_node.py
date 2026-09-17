import json
from core.flow import Node


class LoaderNode(Node):
    def exec(self, state):
        problem_name = state.get("problem_name")
        with open(f"problems/{problem_name}/problem.json") as f:
            state.set("problem_data", json.load(f))
        with open(f"problems/{problem_name}/tests.json") as f:
            state.set("tests_data", json.load(f))
        with open(state.get("solution_path")) as f:
            state.set("user_code", f.read())
        return "ExecNode"