from google.adk.agents import LoopAgent
# from google.adk.agents import Agent 

# 1. Agente Programador
# Toma el contexto de la Fase 1 y genera el código BDI.
agente_programador = Agent(
    name="agente_programador_bdi",
    instructions="""Eres un desarrollador experto en JASON.
    Debes escribir el código para un sistema multi-agente basado en la solicitud original: {prompt_original}.
    Utiliza esta teoría recuperada para no cometer errores de sintaxis: {teoria_jason}
    Guíate por estos ejemplos prácticos: {ejemplos_jason}
    
    Genera el contenido estructurado de los archivos .mas2j y los correspondientes .asl.""",
    output_key="codigo_jason_borrador" # El código generado se guarda aquí para que lo lea el tester
)

# 2. Agente Tester/Revisor
# Prueba el código. Si funciona, rompe el bucle. Si falla, el bucle vuelve a empezar.
agente_tester = Agent(
    name="agente_tester_bdi",
    instructions="""Eres un revisor estricto de código JASON.
    Toma el código generado en el paso anterior y usa la herramienta 'test_mas_code' para compilarlo y probar el SMA[cite: 235].
    
    - Si la salida de la prueba es EXITOSA y no hay errores: Llama a la herramienta 'exit_loop' para terminar el proceso.
    - Si la salida contiene ERRORES: Genera un reporte explicando qué falló para que el programador lo corrija en la siguiente iteración.""",
    tools=["test_mas_code", "exit_loop"], # Usa las tools de testeo y la de salir del bucle
    output_key="resultado_test"
)

# 3. Empaquetar todo en el LoopAgent
# Se ejecutará Programador -> Tester -> Programador -> Tester... hasta un máximo de 5 veces.
flujo_desarrollo = LoopAgent(
    name="flujo_desarrollo_iterativo",
    sub_agents=[agente_programador, agente_tester],
    max_iterations=5  # Condición de salida de seguridad
)