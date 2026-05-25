# agents/orchestrator.py
from google.adk.agents import SequentialAgent
# Importamos los sub-flujos que desarrollará cada miembro del equipo
from agents.researcher import flujo_investigacion  # ParallelAgent (Persona A)
from agents.developer import flujo_desarrollo      # LoopAgent (Persona B)
# Supongamos que definen un agente simple para el guardado final
from agents.saver import agente_guardado          # Agente de guardado final

# El SequentialAgent ejecuta los sub-agentes en un orden predefinido.
# El output de una fase guardado en el 'state' es la entrada de la siguiente.
orquestador_principal = SequentialAgent(
    name="orquestador_bdi_jason",
    sub_agents=[
        flujo_investigacion,  # Paso 1: Paralelo (RAG + GitHub) -> Llena 'contexto_investigacion'
        flujo_desarrollo,     # Paso 2: Bucle (Generar + Testear) -> Llena 'codigo_jason_borrador'
        agente_guardado       # Paso 3: Guardar el MAS verificado en /output 
    ]
)