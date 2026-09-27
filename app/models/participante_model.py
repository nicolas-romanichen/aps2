from pydantic import BaseModel, ConfigDict, EmailStr, Field

class ParticipanteEntrada(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome: str = Field(min_length=1)
    email: EmailStr
    curso: str

class Participante(ParticipanteEntrada):
    id: int
