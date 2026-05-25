# agents/researcher.py
from google.adk.agents import LlmAgent, ParallelAgent
from config_llm import modelo_compartido
from tools.custom_tools import search_github_examples
from rag import search_local_docs

agente_teoria = LlmAgent(
    name="Investigador_Teoria",
    model=modelo_compartido,
    instruction="""Eres un investigador experto en AgentSpeak y Jason. 
    Usa 'search_local_docs' para buscar teoría sobre la solicitud del usuario en: {prompt_original}.
    Extrae la sintaxis clave.""",
    tools=[search_local_docs],
    output_key="teoria_jason"
)

agente_codigo = LlmAgent(
    name="Investigador_Ejemplos",
    model=modelo_compartido,
    instruction="""Eres un buscador de código BDI.
    Usa 'search_github_examples' para encontrar archivos .mas2j y .asl reales relacionados con: {prompt_original}.
    Explora la ruta '' primero y luego entra en los directorios relevantes.""",
    tools=[search_github_examples],
    output_key="ejemplos_jason"
)

# Ejecuta ambos a la vez
flujo_investigacion = ParallelAgent(
    name="flujo_investigacion",
    sub_agents=[agente_teoria, agente_codigo]
)