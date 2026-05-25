# tools/custom_tools.py
import os
import subprocess
import chromadb
import tempfile

# 1. Herramienta de GitHub (Para el ParallelAgent)
def search_github_examples(query: str) -> str:
    """
    Busca ejemplos oficiales de código JASON (BDI) en GitHub basándose en la query.
    Retorna fragmentos de código relevantes.
    """
    base_api_url = "https://api.github.com/repos/jason-lang/jason/contents/examples"
    url = f"{base_api_url}/{path}".strip("/")
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Python-urllib'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if isinstance(data, list):
                items = [f"[{item['type']}] {item['path'].replace('examples/', '', 1)}" for item in data]
                return f"Contenido de '{path or 'raíz'}':\n" + "\n".join(items)
            
            elif isinstance(data, dict) and data.get("type") == "file":
                download_url = data.get("download_url")
                if download_url:
                    req_file = urllib.request.Request(download_url, headers={'User-Agent': 'Python-urllib'})
                    with urllib.request.urlopen(req_file) as f_res:
                        return f_res.read().decode('utf-8')
                return "Error: No se encontró la URL de descarga del archivo."
            else:
                return "Respuesta inesperada de la API de GitHub."
                
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return f"Error: No se encontró la ruta '{path}' en los ejemplos de Jason."
        if e.code == 403:
            return "Error: Límite de peticiones a la API de GitHub excedido. Inténtalo más tarde."
        return f"Error HTTP al acceder a GitHub: {e.code} - {e.reason}"
    except Exception as e:
        return f"Error al intentar acceder a los ejemplos: {e}"


# 2. Herramienta RAG (Para el ParallelAgent)
def search_local_docs(query: str) -> str:
    """
    Busca información en la documentación local de Jason usando ChromaDB.
    """
    try:
        # 1. Inicializar el cliente de ChromaDB apuntando a la base de datos persistente
        client = chromadb.PersistentClient(path="./chroma_db")
        
        # 2. Obtener la colección (asumimos que 'update_rag.py' ya la creó)
        collection = client.get_collection(name="jason_docs")
        
        # 3. Realizar la búsqueda semántica recuperando los top-k fragmentos
        resultados = collection.query(
            query_texts=[query],
            n_results=3 # Devuelve los 3 fragmentos más relevantes
        )
        
        # 4. Formatear los resultados para que el LLM los entienda
        documentos = resultados['documents'][0]
        contexto = "\n\n".join(documentos)
        
        return f"Contexto recuperado de la documentación:\n{contexto}"
    
    except Exception as e:
        return f"Error al buscar en la documentación local: {e}"

# 3. Herramienta de Pruebas (Para el LoopAgent)
def test_mas_code(codigo_mas2j: str, codigos_asl: dict) -> str:
    """
    Guarda y ejecuta el código en un directorio temporal para probar el SMA.
    codigos_asl debe ser un diccionario { 'nombre_agente.asl': 'codigo...' }
    """
    # 1. Crear un directorio temporal que se borrará automáticamente al terminar
    with tempfile.TemporaryDirectory() as temp_dir:
        
        # 2. Escribir el archivo .mas2j
        ruta_mas2j = os.path.join(temp_dir, "test_project.mas2j")
        with open(ruta_mas2j, "w") as f:
            f.write(codigo_mas2j)
            
        # 3. Escribir los archivos .asl
        for nombre_archivo, contenido in codigos_asl.items():
            ruta_asl = os.path.join(temp_dir, nombre_archivo)
            with open(ruta_asl, "w") as f:
                f.write(contenido)
                
        # 4. Ejecutar Jason usando subprocess (requiere que JASON_BIN esté en el PATH)
        try:
            # Ejecutamos jason en modo consola/batch si es posible para que no abra interfaces gráficas
            comando = ["jason", "test_project.mas2j"]
            resultado = subprocess.run(
                comando, 
                cwd=temp_dir,          # Ejecutar dentro del directorio temporal
                capture_output=True,   # Capturar stdout y stderr
                text=True,             # Devolver como string
                timeout=15             # Evitar que se quede colgado
            )
            
            # 5. Devolver el log de la consola para que el Agente Revisor lo analice
            if resultado.returncode == 0:
                return f"ÉXITO. Salida:\n{resultado.stdout}"
            else:
                return f"ERROR DE COMPILACIÓN/EJECUCIÓN. Detalles:\n{resultado.stderr}\n{resultado.stdout}"
                
        except subprocess.TimeoutExpired:
            return "ERROR: La ejecución superó el tiempo límite. Revisa si hay bucles infinitos."
        except Exception as e:
            return f"ERROR DEL SISTEMA al intentar ejecutar jason: {e}"
        
# 4. Herramienta de Guardado Final (Para el Agente Saver)
def save_mas_code(codigo_mas2j: str, codigo_asl: dict) -> str:
    """
    Guarda el MAS completo (.mas2j + .asl) en su propia subcarpeta dentro del directorio 'output'.
    """
    # Lógica para crear la carpeta en /output y escribir los archivos definitivos.
    return "Archivos guardados correctamente en /output/nuevo_proyecto"