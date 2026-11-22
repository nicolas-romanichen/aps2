from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.schemas.evento_schema import EventoEntrada
from app.schemas.participante_schema import ParticipanteEntrada
from app.services.erros import NaoEncontradoError, RegraNegocioError
from app.services.evento_service import EventoService
from app.services.inscricao_service import InscricaoService
from app.services.participante_service import ParticipanteService


def test_evento_inexistente():
    repositorio = Mock()
    repositorio.buscar.return_value = None
    with pytest.raises(NaoEncontradoError):
        EventoService(repositorio, Mock()).buscar(1)


def test_capacidade_menor_que_inscritos(evento):
    repositorio, inscricoes = Mock(), Mock()
    inscricoes.listar_por_evento.return_value = [1, 2]
    with pytest.raises(RegraNegocioError):
        EventoService(repositorio, inscricoes).atualizar(1, EventoEntrada(**(evento | {"capacidade": 1})))
    repositorio.atualizar.assert_not_called()


def test_email_ja_cadastrado(participante):
    repositorio = Mock()
    repositorio.buscar_por_email.return_value = SimpleNamespace(id=1)
    with pytest.raises(RegraNegocioError):
        ParticipanteService(repositorio, Mock()).criar(ParticipanteEntrada(**participante))
    repositorio.criar.assert_not_called()


def test_atualizacao_aceita_email_do_proprio_participante(participante):
    repositorio = Mock()
    repositorio.buscar_por_email.return_value = SimpleNamespace(id=1)
    dados = ParticipanteEntrada(**participante)
    ParticipanteService(repositorio, Mock()).atualizar(1, dados)
    repositorio.atualizar.assert_called_once_with(1, dados)


@pytest.mark.parametrize("duplicada,inscritos", [(True, []), (False, [1])],
                         ids=["inscricao-duplicada", "evento-lotado"])
def test_inscricao_recusada(duplicada, inscritos):
    repositorio, eventos = Mock(), Mock()
    eventos.buscar.return_value.capacidade = 1
    repositorio.existe.return_value = duplicada
    repositorio.listar_por_evento.return_value = inscritos
    with pytest.raises(RegraNegocioError):
        InscricaoService(repositorio, eventos, Mock()).criar(1, 2)
    repositorio.criar.assert_not_called()
