from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

class ParticipanteEntrada(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, from_attributes=True)

    nome: str = Field(min_length=1)
    email: EmailStr
    curso: str

    @field_validator("email")
    @classmethod
    def normalizar_email(cls, valor: str) -> str:
        return valor.lower()

class Participante(ParticipanteEntrada):
    id: int
