# agents/orchestrator.py
from google.adk.agents import LlmAgent, SequentialAgent
from config_llm import modelo_compartido
from .researcher import flujo_investigacion
from .developer import flujo_desarrollo
from tools.custom_tools import save_mas_code

agente_guardado = LlmAgent(
    name="Consolidador",
    model=modelo_compartido,
    instruction="""Toma el código validado final: {codigo_jason_borrador}.
    Usa SÍ O SÍ la herramienta 'save_mas_code' para guardar el proyecto.
    Informa al usuario de que el proceso ha finalizado.""",
    tools=[save_mas_code]
)

# Orden de ejecución estricto: Investigar -> Programar/Probar -> Guardar
orquestador_principal = SequentialAgent(
    name="orquestador_bdi",
    sub_agents=[
        flujo_investigacion,
        flujo_desarrollo,
        agente_guardado
    ]
)