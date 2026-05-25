# from google.adk.agents import Agent 

# Agente Final de Guardado
# Su único objetivo es coger el código que sobrevivió al LoopAgent y guardarlo a disco.
agente_guardado = Agent(
    name="agente_guardado_final",
    instructions="""Eres el encargado de consolidar el proyecto.
    Has recibido el código JASON validado y final: {codigo_jason_borrador}.
    
    Usa la herramienta 'save_mas_code' para guardar este MAS completo (.mas2j y .asl) en su propia subcarpeta dentro del directorio 'output'.
    Asegúrate de estructurar correctamente los parámetros de la herramienta para que genere todos los archivos necesarios.""",
    tools=["save_mas_code"] # Herramienta obligatoria para guardar el resultado final 
)