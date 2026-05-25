from google.adk.agents import LlmAgent, ParallelAgent
from config_llm import modelo_compartido
from tools.custom_tools import search_github_examples
# Dependiendo de tu importación, ajusta la siguiente línea si es necesario
from rag import search_local_docs 

agente_teoria = LlmAgent(
    name="Investigador_Teoria",
    model=modelo_compartido,
    instruction="""Eres un investigador experto en AgentSpeak y Jason. 
    Lee la petición que acaba de hacer el usuario en el chat.
    Usa 'search_local_docs' para buscar teoría sobre esa solicitud.
    Extrae la sintaxis clave.""",
    tools=[search_local_docs],
    output_key="teoria_jason"
)

agente_codigo = LlmAgent(
    name="Investigador_Ejemplos",
    model=modelo_compartido,
    instruction="""Eres un buscador de código BDI.
    Usa 'search_github_examples' para encontrar ejemplos.
    
    REGLA DE ORO: Si tras 3 intentos la herramienta no devuelve código útil o se queda esperando, 
    DETENTE INMEDIATAMENTE. No te quedes atrapado en un bucle.
    Responde con "NO_ENCONTRADO_GITHUB" y termina. El Programador sabrá qué hacer con eso.""",
    tools=[search_github_examples],
    output_key="ejemplos_jason"
)

flujo_investigacion = ParallelAgent(
    name="flujo_investigacion",
    sub_agents=[agente_teoria, agente_codigo]
)