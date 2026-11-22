from app.security import conferir_senha, hasher
from app.services.erros import RegraNegocioError


class UsuarioService:
    def __init__(self, repository):
        self.repository = repository

    def criar(self, dados, perfil="usuario"):
        if self.repository.buscar_por_email(dados.email) is not None:
            raise RegraNegocioError("Já existe um usuário cadastrado com este e-mail.")
        senha_hash = hasher.hash(dados.senha.get_secret_value())
        return self.repository.criar(dados.nome, dados.email, senha_hash, perfil)

    def autenticar(self, dados):
        usuario = self.repository.buscar_por_email(dados.email)
        if usuario and conferir_senha(dados.senha.get_secret_value(), usuario.senha_hash):
            return usuario
        return None
