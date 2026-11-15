class RelatorioService:
    def __init__(self, repository):
        self.repository = repository

    def ocupacao(self):
        return self.repository.ocupacao()

    def categorias(self):
        return self.repository.categorias()

    def cursos(self):
        return self.repository.cursos()
