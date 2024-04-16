import itertools

class Poliza:
    __idGenerador=itertools.count(0)
    def __init__(self, id_cliente, volumen_facturacion, suma_asegurada, limite_anualidad, coberturas, ambito_territorial):
        self._id=next(self.__idGenerador)
        self._id_cliente = id_cliente
        self._volumen_facturacion = volumen_facturacion
        self._suma_asegurada=suma_asegurada
        self._limite_anualidad=limite_anualidad
        self._coberturas=coberturas
        self._ambito_territorial=ambito_territorial

    def toString(self):
        coberturas_str = "\n".join(cobertura.toString() for cobertura in self._coberturas)
        return f"Suma Asegurada: {self._suma_asegurada}\nLimite Anualidad: {self._limite_anualidad}\nCoberturas:\n{coberturas_str}\nÁmbito Territorial: {self._ambito_territorial}"
