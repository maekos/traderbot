
class Indicadores:
    def __init__(self, nombre: str):
        self.nombre = nombre

    def __repr__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

    def results(self):
        raise NotImplementedError

    def calculate(self, df):
        raise NotImplementedError
