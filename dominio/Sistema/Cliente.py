from Actividades import Actividades
from Cobertura import Cobertura
import itertools
from Poliza import Poliza

class Cliente:
    __idGenerador=itertools.count(0)
    def __init__(self, nombre, volumen_facturacion, actividades):
        self._id=next(self.__idGenerador)
        self._nombre=nombre
        self._volumen_facturacion=volumen_facturacion
        self._actividades=actividades
        self._polizas=[]
        self._agravada=0