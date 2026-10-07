from dominio.registro_tiempo import RegistroTiempo
from dominio.validador_entrada import ValidadorEntrada as Val

#aqui se compe regisros de tiempo con proyecto 1 - 0..*
class Proyecto:
    def __init__(self, nombre: str, presupuesto: float, descripcion: str = "",
                fecha_inicio: str = "", id: int = None):
        self._id = id
        self._nombre = Val.validar_texto_no_vacio(nombre, "El nombre del proyecto")
        self._descripcion = Val.validar_texto_opcional(descripcion)
        self._fecha_inicio = Val.validar_fecha(fecha_inicio)
        self._presupuesto = Val.validar_monto(presupuesto, "El presupuesto")
        self._registros: list[RegistroTiempo] = []
        self._empleados: list = []                       # asociación Empleado 0..* — 0..* Proyecto

    @property
    def id(self): return self._id
    @id.setter
    def id(self, nuevo_id): self._id = nuevo_id

    @property
    def nombre(self) -> str: return self._nombre

    @property
    def descripcion(self) -> str: return self._descripcion

    @property
    def fecha_inicio(self) -> str: return self._fecha_inicio

    @property
    def presupuesto(self) -> float: return self._presupuesto
    @presupuesto.setter
    def presupuesto(self, monto: float):
        self._presupuesto = Val.validar_monto(monto, "El presupuesto")

    def editar(self, nombre: str, descripcion: str) -> None:
        nombre = Val.validar_texto_no_vacio(nombre, "El nombre del proyecto")
        self._nombre, self._descripcion = nombre, Val.validar_texto_opcional(descripcion)

#Relación con RegistroTiempo 
    def agregar_registro_tiempo(self, registro: RegistroTiempo) -> bool:
        if any(r.id is not None and r.id == registro.id for r in self._registros):
            return False
        self._registros.append(registro)
        return True

    @property
    def registros(self) -> tuple:
        return tuple(self._registros)

    def total_horas(self) -> float:
        return sum(r.horas for r in self._registros)

#Relación con Empleado 
    def agregar_empleado(self, empleado) -> bool:
        if any(e.id == empleado.id for e in self._empleados):
            return False
        self._empleados.append(empleado)
        return True

    def remover_empleado(self, empleado) -> bool:
        for e in self._empleados:
            if e.id == empleado.id:
                self._empleados.remove(e)
                return True
        return False

    @property
    def empleados(self) -> tuple:
        return tuple(self._empleados)

    def mostrar_datos(self) -> str:
        return (f"ID: {self._id} | Proyecto: {self._nombre} | Inicio: {self._fecha_inicio} "
                f"| Presupuesto: ${self._presupuesto:,.2f} | Descripción: {self._descripcion or '-'}")
