import os
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm

# Nos aseguramos de cargar el .env
load_dotenv()

# Recuperamos la clave desde tu archivo .env
# Asegúrate de tener POLIGPT_API_KEY=sk-... en tu .env
api_key_upv = os.getenv("POLIGPT_API_KEY")

if not api_key_upv:
    print("⚠️ AVISO: No se encontró la API Key en el archivo .env. Asegúrate de tenerla configurada.")

# Configuramos el modelo compartido usando la conexión exacta que les dio la universidad
modelo_compartido = LiteLlm(
    model="openai/Qwen3.6-35B-A3B-FP8",
    api_base="https://api.poligpt.upv.es/",
    api_key=api_key_upv
)