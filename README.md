# PocketFlow Code Validator

An AI-powered code evaluation engine. It runs a solution's test cases in an isolated subprocess, then sends the code and results to Google's Gemini API for a structured review of correctness, efficiency, and readability — similar to how a competitive programming judge works, paired with AI-generated feedback.

Built with a custom node/flow engine inspired by the PocketFlow pattern, not an external dependency.

![Demo](docs/demo.gif)

---

## 🔄 Features

- Loads a problem's description and test cases from JSON, and reads the target solution file
- Runs the solution in an isolated subprocess with a timeout, plus memory/CPU limits on Unix systems — the real defense against a broken or resource-heavy submission
- Applies an import-policy check that rejects modules like `subprocess`, `socket`, or `ctypes` before running. This is a linter-level guardrail against obvious misuse, not a security boundary — it won't stop a deliberate attempt to escape via Python's introspection features, and it's meant for evaluating your own practice solutions, not accepting arbitrary code from untrusted strangers
- Sends the code and test results to Gemini (`gemini-flash-latest` by default, falling back to `gemini-flash-lite-latest` on repeated failures) for a structured review: score, correctness, efficiency, readability, and suggestions
- The model can be overridden via an optional `GEMINI_MODEL` environment variable, for API keys with billing enabled that want to use a paid model like `gemini-pro-latest`
- Ships with a sample "Two Sum" problem to validate the full pipeline end to end

---

## 🛠️ Tech stack

- Python 3.9+
- [google-genai](https://pypi.org/project/google-genai/) — Gemini API client
- [python-dotenv](https://pypi.org/project/python-dotenv/) — loads `.env` locally
- Custom node/flow orchestration engine (`core/flow.py`), inspired by PocketFlow's architecture

---

## ⚙️ Setup instructions

1. Clone the repo:

```
git clone https://github.com/jorgegmch/pocketflow-code-validator.git
```

2. Create and activate a virtual environment:

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and add your [Google AI Studio](https://aistudio.google.com/app/apikey) API key:

```
GOOGLE_API_KEY="your-gemini-api-key-here"

# Optional. Overrides the default free-tier model (gemini-flash-latest).
# Set this to a paid model (e.g. gemini-pro-latest) if your API key has billing enabled.
# GEMINI_MODEL="gemini-pro-latest"
```

---

## 🧭 Usage

Run the pipeline against the sample problem:

```bash
python main.py
```

This evaluates `problems/two_sum/solution.py` and prints the test results plus the AI feedback.

To evaluate a different problem, add a `problem.json`, `tests.json`, and `solution.py` under `problems/<name>/`, and point `problem_name` / `solution_path` in `main.py` at it. There's no CLI flag yet — the target problem is set directly in `main.py`.

---

## 📁 Project structure

```
pocketflow-code-validator
├── core/
│   ├── __init__.py
│   └── flow.py
├── evaluator/
│   ├── __init__.py
│   └── runner.py
├── llm/
│   ├── __init__.py
│   └── gemini_client.py
├── nodes/
│   ├── __init__.py
│   ├── loader_node.py
│   ├── exec_node.py
│   └── llm_node.py
├── problems/
│   └── two_sum/
│       ├── problem.json
│       ├── tests.json
│       └── solution.py
├── .env.example
├── .gitignore
├── docs/
│   └── demo.gif
├── main.py
├── README.md
└── requirements.txt
```

---

## License

MIT — see [LICENSE](LICENSE) for details.

Built by [Jorge Gomez](https://github.com/jorgegmch)