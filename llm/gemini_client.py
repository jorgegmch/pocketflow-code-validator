import os, json, time
from google import genai

DEFAULT_MODEL = "gemini-flash-latest"
FALLBACK_MODEL = "gemini-flash-lite-latest"


class GeminiClient:
    def __init__(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("⚠️ No se encontró la variable GOOGLE_API_KEY")

        self.client = genai.Client(api_key=api_key)

        primary = os.environ.get("GEMINI_MODEL", DEFAULT_MODEL)
        self.models_to_try = [primary] if primary == FALLBACK_MODEL else [primary, FALLBACK_MODEL]

    def evaluate_code(self, code: str, problem_desc: str, passed: bool):
        prompt = f"""
        Actúa como un Senior Software Engineer.
        Evalúa este código Python para el problema: '{problem_desc}'
        ¿Pasó los tests técnicos?: {passed}
        
        Código del usuario:
        {code}
        
        Responde ÚNICAMENTE con un JSON puro con esta estructura:
        {{
            "Score": (int entre 0 y 100),
            "Correctness": "explicación",
            "Efficiency": "análisis Big O",
            "Readability": "comentario",
            "Suggestions": ["lista de strings"]
        }}
        """

        for model_id in self.models_to_try:
            for attempt in range(2):
                try:
                    response = self.client.models.generate_content(
                        model=model_id,
                        contents=prompt
                    )

                    text = response.text
                    if "```json" in text:
                        text = text.split("```json")[1].split("```")[0]
                    elif "```" in text:
                        text = text.split("```")[1].split("```")[0]

                    return json.loads(text.strip())

                except Exception as e:
                    if "429" in str(e) or "503" in str(e):
                        print(f"⚠️ {model_id} (intento {attempt+1}): {e}")
                        print("   Esperando 12s...")
                        time.sleep(12)
                    else:
                        print(f"❌ Error con {model_id}: {e}")
                        break  # pasa al siguiente modelo sin agotar los intentos aquí

        return {"Score": 0, "Correctness": "No se pudo conectar con Gemini"}