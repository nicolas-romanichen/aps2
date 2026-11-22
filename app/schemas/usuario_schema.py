from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, field_validator


class Credenciais(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    senha: SecretStr

    @field_validator("email")
    @classmethod
    def normalizar_email(cls, valor: str) -> str:
        return valor.lower()


class UsuarioEntrada(Credenciais):
    nome: str = Field(min_length=1)
    senha: SecretStr = Field(min_length=8, max_length=128)

    @field_validator("nome", mode="before")
    @classmethod
    def limpar_nome(cls, valor):
        return valor.strip() if isinstance(valor, str) else valor

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, valor: SecretStr) -> SecretStr:
        if not valor.get_secret_value().strip():
            raise ValueError("A senha precisa conter caracteres além de espaços.")
        return valor


class UsuarioPublico(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: EmailStr
    perfil: Literal["usuario", "administrador"]


class Token(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
