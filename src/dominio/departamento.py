from dominio.empleado import Empleado
from dominio.validador_entrada import ValidadorEntrada as Val


class Departamento:
    def __init__(self, nombre: str, gerente: Empleado = None, id: int = None):
        self._id = id
        self._nombre = Val.validar_texto_no_vacio(nombre, "El nombre del departamento")
        self._gerente = None
        self.gerente = gerente
        self._empleados: list[Empleado] = []

    @property
    def id(self): return self._id
    @id.setter
    def id(self, nuevo_id): self._id = nuevo_id

    @property
    def nombre(self) -> str: return self._nombre
    @nombre.setter
    def nombre(self, nuevo: str):
        self._nombre = Val.validar_texto_no_vacio(nuevo, "El nombre del departamento")

    @property
    def gerente(self):
        return self._gerente
    @gerente.setter
    def gerente(self, empleado) -> None:
        if empleado is not None and not isinstance(empleado, Empleado):
            raise ValueError("El gerente debe ser un empleado.")
        self._gerente = empleado

    @staticmethod
    def _es_el_mismo(a: Empleado, b: Empleado) -> bool:
        return a is b or (a.id is not None and a.id == b.id)

    # --- Relación con Empleado ---
    def agregar_empleado(self, empleado: Empleado) -> bool:
        if any(self._es_el_mismo(e, empleado) for e in self._empleados):   # no duplica al mismo empleado
            return False
        self._empleados.append(empleado)
        return True

    def remover_empleado(self, empleado: Empleado) -> bool:
        for e in self._empleados:
            if self._es_el_mismo(e, empleado):
                self._empleados.remove(e)
                return True
        return False

    @property
    def empleados(self) -> tuple:
        return tuple(self._empleados)

    def cantidad_empleados(self) -> int:
        return len(self._empleados)

    def mostrar_datos(self) -> str:
        gerente = self._gerente.nombre if self._gerente else "Sin gerente"
        return f"ID: {self._id} | Departamento: {self._nombre} | Gerente: {gerente}"