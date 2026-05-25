import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 1. TRUCO DE RUTAS AVANZADO: Forzamos a Python a mirar primero en estas carpetas
directorio_actual = str(Path(__file__).parent)
raiz_proyecto = str(Path(__file__).parent.parent)

# Insertar en la posición 0 da máxima prioridad a tus carpetas
if directorio_actual not in sys.path:
    sys.path.insert(0, directorio_actual)
if raiz_proyecto not in sys.path:
    sys.path.insert(0, raiz_proyecto)

# 2. Cargar el entorno desde la raíz
load_dotenv(os.path.join(raiz_proyecto, ".env"))

# 3. Registrar el modelo OpenAI/Qwen
try:
    from typing import override
except ImportError:
    from typing_extensions import override

from google.adk.models.lite_llm import LiteLlm
from google.adk.models.registry import LLMRegistry

class OpenAiLiteLlm(LiteLlm):
    @classmethod
    @override
    def supported_models(cls):
        return [r"openai/.*"]

LLMRegistry.register(OpenAiLiteLlm)

# 4. IMPORTAR EL ORQUESTADOR
from .orchestator import orquestador_principal

# 5. EXPOSICIÓN FINAL
root_agent = orquestador_principal