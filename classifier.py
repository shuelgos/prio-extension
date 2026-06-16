from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL
from models import ClassifyRequest, ClassifyResponse
import json

# Inicializamos el cliente de Groq
client = Groq(api_key=GROQ_API_KEY)

def classify_email(request: ClassifyRequest) -> ClassifyResponse:
    
    # Construimos el prompt dinámico con las áreas del usuario

    areas_list = ", ".join(request.areas)
    
    prompt = f"""
    Eres un asistente experto en clasificación de emails de soporte al cliente.
    
    Analiza el siguiente email y responde ÚNICAMENTE con un JSON válido, sin texto adicional.
    
    Las áreas disponibles son: {areas_list}
    
    Email a analizar:
    Asunto: {request.email_subject}
    Contenido: {request.email_text}
    
    Responde con este formato JSON exacto:
    {{
        "area": "una de las áreas disponibles",
        "urgencia": "Urgente | Normal | Informativo | Spam",
        "resumen": "resumen del email en máximo 2 líneas",
        "razones": [
            "razón 1 por la que se clasificó así",
            "razón 2",
            "razón 3"
        ],
        "respuesta_sugerida": "respuesta profesional sugerida para este email"
    }}
    """
    
    # Le preguntamos a Groq
    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Eres un clasificador de emails. Respondes SOLO con JSON válido, sin explicaciones ni texto adicional."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1  # bajo para respuestas consistentes y predecibles
    )
    
    # Extraemos la respuesta
    response_text = completion.choices[0].message.content
    
    # Convertimos el JSON string a diccionario Python
    response_data = json.loads(response_text)
    
    # Devolvemos la respuesta en el formato oficial de Prio
    return ClassifyResponse(
        area=response_data["area"],
        urgencia=response_data["urgencia"],
        resumen=response_data["resumen"],
        razones=response_data["razones"],
        respuesta_sugerida=response_data["respuesta_sugerida"]
    )