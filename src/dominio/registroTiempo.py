class RegistroTiempo:

    def __init__(self, fecha: str, horas: float):
        self.fecha = fecha
        self.horas = horas
        self._registros: list = []

    def mostrardatos(self) -> str:
        return f"{self.fecha} {self.horas}"

    def mostrardatos2(self, hola: str) -> str:
        return f"///////  {self.fecha} {hola}"

    def agregar_registrotiempo(self, registrotiempo) -> bool:
        if registrotiempo in self._registros:
            return False

        self._registros.append(registrotiempo)
        return True

    @property
    def registros(self) -> tuple:
        return tuple(self._registros)

    def cantidad_registros(self) -> int:
        return len(self._registros)