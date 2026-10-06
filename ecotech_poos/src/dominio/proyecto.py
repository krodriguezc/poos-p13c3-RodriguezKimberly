from dominio.registroTiempo import RegistroTiempo
from dominio.validador_entrada import ValidadorEntrada


class Proyecto:
    """Iniciativa de la empresa. Compone sus registros de tiempo (composición 1 — 0..*)."""

    def __init__(self, nombre: str, presupuesto: float, id: int = None):
        self._id = id
        self._nombre = ValidadorEntrada.validar_texto_no_vacio(nombre, "El nombre del proyecto")
        self._presupuesto = ValidadorEntrada.validar_monto(presupuesto, "El presupuesto")
        self._registros: list[RegistroTiempo] = []
        self._empleados: list = []                       

    @property
    def id(self): return self._id
    @id.setter
    def id(self, nuevo_id): self._id = nuevo_id

    @property
    def nombre(self) -> str: return self._nombre
    @nombre.setter
    def nombre(self, nuevo: str):
        self._nombre = ValidadorEntrada.validar_texto_no_vacio(nuevo, "El nombre del proyecto")

    @property
    def presupuesto(self) -> float: return self._presupuesto
    @presupuesto.setter
    def presupuesto(self, monto: float):
        self._presupuesto = ValidadorEntrada.validar_monto(monto, "El presupuesto")

    def agregar_registro_tiempo(self, registro: RegistroTiempo) -> None:
        self._registros.append(registro)

    @property
    def registros(self) -> tuple:
        return tuple(self._registros)

    def agregar_empleado(self, empleado) -> bool:
        if any(e.id == empleado.id for e in self._empleados):
            return False
        self._empleados.append(empleado)
        return True

    def quitar_empleado(self, empleado) -> bool:
        for e in self._empleados:
            if e.id == empleado.id:
                self._empleados.remove(e)
                return True
        return False

    @property
    def empleados(self) -> tuple:
        return tuple(self._empleados)

    def total_horas(self) -> float:
        return sum(r.horas for r in self._registros)

    def mostrar_datos(self) -> str:
        return f"ID: {self._id} | Proyecto: {self._nombre} | Presupuesto: ${self._presupuesto:,.2f}"
