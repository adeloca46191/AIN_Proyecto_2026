# agent.py
import os
from dotenv import load_dotenv

# 1. Cargar el entorno
load_dotenv()

# 2. Registrar el modelo OpenAI/Qwen
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

# 3. Importar tus Workflows (Flujos)
from agents.researcher import flujo_investigacion
from agents.developer import flujo_desarrollo
from agents.orchestrator import orquestador_principal

# =====================================================================
# 4. EXPOSICIÓN DE AGENTES PARA EL MENÚ DEL ADK WEB
# Todas las variables globales aquí abajo que contengan un agente
# aparecerán automáticamente como opciones en la interfaz gráfica.
# =====================================================================

# Opción A: El sistema completo (El que usarás para la evaluación)
Orquestador_Completo = orquestador_principal

# Opción B: Solo el flujo de investigación (Para probar el RAG y GitHub)
Investigador_Teoria = flujo_investigacion

# Opción C: Solo el flujo de código (Para probar el bucle de compilación)
Desarrollador_Iterativo = flujo_desarrollo