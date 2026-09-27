from datetime import date, time

from pydantic import BaseModel, ConfigDict, Field

class EventoEntrada(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    titulo: str = Field(min_length=1)
    descricao: str
    data: date
    horario: time
    local: str
    capacidade: int = Field(gt=0, strict=True)
    categoria: str

class Evento(EventoEntrada):
    id: int
