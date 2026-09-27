from app.models.inscricao_model import Inscricao

class InscricaoRepository:
    def __init__(self):
        self._inscricoes: dict[tuple[int, int], Inscricao] = {}

    def criar(self, evento_id: int, participante_id: int) -> Inscricao:
        inscricao = Inscricao(evento_id=evento_id, participante_id=participante_id)
        self._inscricoes[evento_id, participante_id] = inscricao
        return inscricao

    def existe(self, evento_id: int, participante_id: int) -> bool:
        return (evento_id, participante_id) in self._inscricoes

    def listar_por_evento(self, evento_id: int) -> list[Inscricao]:
        return [i for i in self._inscricoes.values() if i.evento_id == evento_id]

    def remover_por_evento(self, evento_id: int) -> None:
        for chave in list(self._inscricoes):
            if chave[0] == evento_id:
                del self._inscricoes[chave]

    def remover_por_participante(self, participante_id: int) -> None:
        for chave in list(self._inscricoes):
            if chave[1] == participante_id:
                del self._inscricoes[chave]
