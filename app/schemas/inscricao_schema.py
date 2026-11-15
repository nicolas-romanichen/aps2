from datetime import date
from pydantic import BaseModel, ConfigDict

class Inscricao(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    evento_id: int
    participante_id: int
    data_inscricao: date
