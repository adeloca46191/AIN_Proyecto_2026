import os
from dotenv import load_dotenv

# 1. Cargar las variables de entorno (API keys de .env)
load_dotenv()

# 2. Registrar el adaptador para modelos OpenAI/Qwen en el ADK
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

# 3. Importar el orquestador principal
from agents.orchestrator import orquestador_principal

# 4. Exponer el agente para la interfaz web
# En la mayoría de implementaciones ADK con interfaz web, el framework busca 
# una variable principal (suele llamarse 'agent', 'app' o 'orquestador').
# Asignamos nuestro workflow principal a la variable que el ADK Web espera leer:
agent = orquestador_principal

print("[INFO] Entorno cargado y LLM registrado.")
print("[INFO] Orquestador listo. Inicia la interfaz web del ADK para comenzar a chatear.")