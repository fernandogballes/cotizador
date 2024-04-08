class Cobertura:
    def __init__(self, nombre, sublimite, franquicia):
        self._nombre = nombre
        self._sublimite = sublimite
        self._franquicia = franquicia

    def toString(self):
        return f"{self._nombre}\n\tSublímite: {self._sublimite}\n\tFranquicia: {self._franquicia}"