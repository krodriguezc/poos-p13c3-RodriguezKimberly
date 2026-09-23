from dominio.empleado import Empleado


class Departamento:

    def __init__(self, nombre: str):
        self._nombre = nombre
        self._empleados: list[Empleado] = []

    @property
    def nombre(self) -> str:
        return self._nombre

    def agregar_empleado(self, empleado: Empleado) -> bool:
        if empleado in self._empleados:
            return False
        self._empleados.append(empleado)
        return True

    @property
    def empleados(self) -> tuple:
        return tuple(self._empleados)

    def cantidad_empleados(self) -> int:
        return len(self._empleados)