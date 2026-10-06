from dominio.empleado import Empleado
from dominio.validador_entrada import ValidadorEntrada


class Departamento:
    """Agrupa empleados (agregación 1 — 0..*): el empleado existe aunque no haya departamento."""

    def __init__(self, nombre: str, id: int = None):
        self._id = id
        self._nombre = ValidadorEntrada.validar_texto_no_vacio(nombre, "El nombre del departamento")
        self._empleados: list[Empleado] = []

    @property
    def id(self): return self._id
    @id.setter
    def id(self, nuevo_id): self._id = nuevo_id

    @property
    def nombre(self) -> str: return self._nombre
    @nombre.setter
    def nombre(self, nuevo: str):
        self._nombre = ValidadorEntrada.validar_texto_no_vacio(nuevo, "El nombre del departamento")

    def agregar_empleado(self, empleado: Empleado) -> bool:
        if empleado in self._empleados:      
            return False
        self._empleados.append(empleado)
        return True

    def quitar_empleado(self, empleado: Empleado) -> bool:
        if empleado not in self._empleados:
            return False
        self._empleados.remove(empleado)
        return True

    @property
    def empleados(self) -> tuple:
        return tuple(self._empleados)

    def cantidad_empleados(self) -> int:
        return len(self._empleados)

    def mostrar_datos(self) -> str:
        return f"ID: {self._id} | Departamento: {self._nombre}"
