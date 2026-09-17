import ast
import json
import os
import subprocess
import sys
import tempfile

# Módulos de sistema/red bloqueados por política del validador, no por seguridad real.
# os y sys quedan permitidos porque tienen usos legítimos comunes.
FORBIDDEN_MODULES = {
    "subprocess", "socket", "ctypes", "shutil",
    "multiprocessing", "ftplib", "smtplib", "ssl",
}
FORBIDDEN_CALLS = {"eval", "exec", "compile", "__import__"}


def passes_import_policy(source: str) -> tuple[bool, str]:
    """Linter de imports/llamadas prohibidas. No es un sandbox."""
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return False, f"Código con error de sintaxis: {e}"

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in FORBIDDEN_MODULES:
                    return False, f"Import no permitido: '{alias.name}'"
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in FORBIDDEN_MODULES:
                return False, f"Import no permitido: '{node.module}'"
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in FORBIDDEN_CALLS:
                return False, f"Llamada no permitida: '{node.func.id}'"

    return True, ""


class IsolatedRunner:
    """Corre la solución en un proceso aparte, con límites de tiempo y recursos.
    No reemplaza un sandbox real, solo aísla del proceso principal."""

    def run(self, file_path, entrypoint, inputs):
        with open(file_path) as f:
            source = f.read()

        allowed, reason = passes_import_policy(source)
        if not allowed:
            return False, None, reason

        # resource solo existe en Unix; en Windows queda solo el timeout
        wrapper = f"""
import json, importlib.util

try:
    import resource
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
except ImportError:
    pass

try:
    spec = importlib.util.spec_from_file_location("mod", r"{file_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    res = getattr(mod, "{entrypoint}")(**{inputs})
    print(json.dumps({{"s": True, "r": res}}))
except Exception as e:
    print(json.dumps({{"s": False, "e": str(e)}}))
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(wrapper)
            tmp_path = f.name

        try:
            # sys.executable evita depender de que "python3" exista como comando
            proc = subprocess.run([sys.executable, tmp_path], capture_output=True, text=True, timeout=5)
            data = json.loads(proc.stdout.strip())
            return data["s"], data.get("r"), data.get("e", "")
        except Exception as e:
            return False, None, str(e)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)