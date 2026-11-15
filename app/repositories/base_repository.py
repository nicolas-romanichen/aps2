from sqlalchemy import select

class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    def criar(self, dados):
        registro = self.model(**dados.model_dump())
        self.session.add(registro)
        self.session.flush()
        return registro

    def listar(self):
        return list(self.session.scalars(select(self.model).order_by(self.model.id)))

    def buscar(self, id):
        return self.session.get(self.model, id)

    def atualizar(self, id, dados):
        registro = self.buscar(id)
        for campo, valor in dados.model_dump().items():
            setattr(registro, campo, valor)
        self.session.flush()
        return registro

    def remover(self, id):
        self.session.delete(self.buscar(id))
        self.session.flush()
