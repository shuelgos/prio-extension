from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

#Clasificamos 
class ClassifyRequest (BaseModel):
    email_text: str
    areas: list[str]
    email_subject: Optional [str] = ""
    
class ClasifyResponse (BaseModel):
    area: str
    urgencia: str
    resumen: str
    razones: list[str]
    repuesta_sugerida: str
 
#guardamos en SQLite   
class ClasificationRecord (BaseModel):
    id: Optional [int] = None
    email_subject: str
    area: str
    urgencia: str
    resumen: str
    created_at: Optional [datetime] = None         