from core.flow import Node
from llm.gemini_client import GeminiClient


class LLMNode(Node):
    def exec(self, state):
        print("--- Consultando IA ---")
        client = GeminiClient()
        feedback = client.evaluate_code(
            state.get("user_code"),
            state.get("problem_data")["description"],
            state.get("all_passed"),
        )
        print(f"\n🚀 RESULTADOS:\nTests Pasados: {state.get('all_passed')}\nScore: {feedback.get('Score')}/100")
        print(f"Feedback: {feedback.get('Correctness')}")
        return None