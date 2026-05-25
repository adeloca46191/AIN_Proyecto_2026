import os
from dotenv import load_dotenv
# Importamos el orquestador principal que definirá el SequentialAgent
from agents.orchestrator import orquestador_principal

def main():
    # 1. Cargar las variables de entorno del archivo .env (API_KEY, rutas, etc.) [cite: 166]
    load_dotenv()
    
    print("====================================================================")
    print("=== Sistema Multi-Agente ADK - Generador de Razonadores BDI JASON ===")
    print("====================================================================\n")
    
    # 2. Definir el prompt del usuario (Aquí pueden cambiarlo según el caso de evaluación)
    # Ejemplo con el Caso 1: Serie de Fibonacci [cite: 271]
    prompt_usuario = "Crea un agente que imprima la serie de Fibonacci hasta el valor 100." [cite: 271]
    
    # 3. Inicializar el Estado (Memoria Compartida)
    # El estado es un diccionario de Python accesible y modificable por todos los agentes .
    # Sirve para almacenar información clave que persiste entre pasos[cite: 55].
    session_state = {
        "prompt_original": prompt_usuario,      # Entrada inicial de la petición
        "contexto_investigacion": "",            # Aquí el ParallelAgent guardará la documentación/ejemplos recuperados
        "codigo_jason_borrador": "",             # Aquí el LoopAgent escribirá el código generado (.mas2j y .asl)
        "resultado_test": "",                    # Almacena el log/resultado de test_mas_code [cite: 235]
        "intento_actual": 0                      # Contador para no superar el límite de 5 intentos de testeo [cite: 236]
    }
    
    print(f"[INPUT] Prompt del usuario: '{prompt_usuario}'\n")
    print("[INFO] Iniciando el flujo de trabajo secuencial...")
    
    try:
        # 4. Invocar al agente secuencial pasándole el estado inicial
        # El framework ADK ejecutará la lista de sub-agentes en el orden establecido[cite: 89].
        # Nota: Ajusta el método de ejecución (ej. .run() o .execute()) según la firma exacta de su SDK instalado.
        resultado = orquestador_principal.run(state=session_state)
        
        print("\n====================================================================")
        print("=== [ÉXITO] El proceso ha terminado correctamente ===")
        print("Los archivos finales se han guardado en la carpeta /output.") [cite: 237]
        print("====================================================================")
        
    except Exception as e:
        print(f"\n[ERROR] Ocurrió un fallo crítico durante la ejecución del workflow: {e}")

if __name__ == "__main__":
    main()