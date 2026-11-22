from sqlalchemy import select

from app.models.usuario_model import Usuario


class UsuarioRepository:
    def __init__(self, session):
        self.session = session

    def buscar(self, usuario_id):
        return self.session.get(Usuario, usuario_id)

    def buscar_por_email(self, email):
        return self.session.scalar(select(Usuario).where(Usuario.email == email))

    def criar(self, nome, email, senha_hash, perfil):
        usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash, perfil=perfil)
        self.session.add(usuario)
        self.session.flush()
        return usuario
