class Proyecto:

    def __init__(self, nombre: str, presupuesto: float, id=None):
        self._id = id
        self._nombre = nombre
        self._presupuesto = presupuesto

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, nuevo_id):
        self._id = nuevo_id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def presupuesto(self) -> float:
        return self._presupuesto

    def mostrar_datos(self) -> str:
        return f"Proyecto: {self._nombre} | Presupuesto: ${self._presupuesto:,.2f}"
