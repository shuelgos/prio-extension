from dotenv import load_dotenv
import os

# Carga las variables del archivo .env
# Es como abrir el panel de control antes de arrancar
load_dotenv()

# API Key de Groq — la leemos del .env, nunca hardcodeada
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# llama-3.3-70b es potente y está en el tier gratuito
GROQ_MODEL = "llama-3.3-70b-versatile"

# Nombre de la base de datos SQLite
DATABASE_URL = "prio.db"

# Validación — si no hay API key, el servidor no arranca
if not GROQ_API_KEY:
    raise ValueError("No encontré GROQ_API_KEY en el .env")