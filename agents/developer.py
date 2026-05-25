from google.adk.agents import LlmAgent, LoopAgent
from config_llm import modelo_compartido
from tools.custom_tools import test_mas_code

def exit_loop() -> str:
    """Llama a esta herramienta EXCLUSIVAMENTE cuando el código haya compilado con 'ÉXITO' para terminar la validación."""
    return "BUCLE_FINALIZADO"

agente_programador = LlmAgent(
    name="Programador_BDI",
    model=modelo_compartido,
    instruction="""Eres un programador experto en MAS BDI.
    Crea el código para cumplir con la petición del usuario del chat.
    Basate en esta teoría: {teoria_jason} y estos ejemplos: {ejemplos_jason}.
    
    REGLAS ESTRICTAS:
    1. MAS nombre_proyecto { infrastructure: Centralised agents: nombre; }
    2. Las variables empiezan con Mayúscula. 
    3. Todos los planes terminan en PUNTO (.).
    4. Genera el código estructurado en formato JSON o como texto claro.
    
    Si vienes de un error previo, arréglalo.""",
    output_key="codigo_jason_borrador"
)

agente_tester = LlmAgent(
    name="Tester_BDI",
    model=modelo_compartido,
    instruction="""Analiza el código generado.
    Usa 'test_mas_code' para compilarlo.
    
    - Si la consola devuelve 'ÉXITO', usa 'exit_loop' para terminar.
    - Si devuelve 'ERROR', no salgas del bucle e informa del fallo.
    
    NUNCA añadas el token '<|channel|>commentary' al usar herramientas.""",
    tools=[test_mas_code, exit_loop],
    output_key="resultado_test"
)

flujo_desarrollo = LoopAgent(
    name="flujo_programacion",
    sub_agents=[agente_programador, agente_tester],
    max_iterations=5
)