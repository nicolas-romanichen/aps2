from getpass import getpass

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import UsuarioEntrada
from app.services.erros import RegraNegocioError
from app.services.usuario_service import UsuarioService
from database.db import Session, criar_tabelas, db


def main():
    try:
        dados = UsuarioEntrada(nome=input("Nome: "), email=input("E-mail: "), senha=getpass("Senha: "))
    except ValidationError:
        raise SystemExit("Confira nome, e-mail e senha (8 a 128 caracteres).") from None
    criar_tabelas(db)
    try:
        with Session.begin() as session:
            UsuarioService(UsuarioRepository(session)).criar(dados, perfil="administrador")
    except (RegraNegocioError, IntegrityError):
        raise SystemExit("Já existe uma conta com esse e-mail.") from None
    print("Administrador cadastrado.")


if __name__ == "__main__":
    main()
