from core.flow import Node
from evaluator.runner import IsolatedRunner


class ExecNode(Node):
    def exec(self, state):
        runner = IsolatedRunner()
        problem_data = state.get("problem_data")
        tests = state.get("tests_data")["tests"]
        solution_path = state.get("solution_path")

        all_passed = True
        results = []
        for t in tests:
            ok, res, err = runner.run(solution_path, problem_data["entrypoint"], t["input"])
            passed = ok and res == t["expected"]
            if not passed:
                all_passed = False
            results.append({"in": t["input"], "out": res if ok else err, "pass": passed})

        state.set("all_passed", all_passed)
        state.set("results", results)
        return "LLMNode"