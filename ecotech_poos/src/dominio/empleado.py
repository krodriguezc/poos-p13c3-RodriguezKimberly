from abc import ABC, abstractmethod

from dominio.registroTiempo import RegistroTiempo
from dominio.validador_entrada import ValidadorEntrada


class Empleado(ABC):
    def __init__(self, rut: str, nombre: str, correo: str = "", departamento_id: int = None,
                salario_base: float = 0.0, id: int = None):
        self._id = id
        self._rut = ValidadorEntrada.validar_rut(rut)
        self._nombre = ValidadorEntrada.validar_texto_no_vacio(nombre, "El nombre")
        self._correo = ValidadorEntrada.validar_email_opcional(correo)
        self._departamento_id = departamento_id
        self._salario_base = ValidadorEntrada.validar_monto(salario_base, "El salario")
        self._registros_tiempo: list[RegistroTiempo] = []
        self._proyectos: list = []                     

    @property
    def id(self): return self._id
    @id.setter
    def id(self, nuevo_id): self._id = nuevo_id

    @property
    def rut(self) -> str: return self._rut        

    @property
    def nombre(self) -> str: return self._nombre
    @nombre.setter
    def nombre(self, nuevo: str): self._nombre = ValidadorEntrada.validar_texto_no_vacio(nuevo, "El nombre")

    @property
    def correo(self) -> str: return self._correo
    @correo.setter
    def correo(self, nuevo: str): self._correo = ValidadorEntrada.validar_email_opcional(nuevo)

    @property
    def departamento_id(self): return self._departamento_id
    @departamento_id.setter
    def departamento_id(self, dep_id): self._departamento_id = dep_id

    @property
    def salario_base(self) -> float: return self._salario_base
    @salario_base.setter
    def salario_base(self, monto: float): self._salario_base = ValidadorEntrada.validar_monto(monto, "El salario")

    def agregar_registro_tiempo(self, registro: RegistroTiempo) -> None:
        self._registros_tiempo.append(registro)

    @property
    def registros_tiempo(self) -> tuple:
        return tuple(self._registros_tiempo)       

    def total_horas(self) -> float:
        return sum(r.horas for r in self._registros_tiempo)

    def agregar_proyecto(self, proyecto) -> bool:
        if any(p.id == proyecto.id for p in self._proyectos):
            return False
        self._proyectos.append(proyecto)
        return True

    def quitar_proyecto(self, proyecto) -> bool:
        for p in self._proyectos:
            if p.id == proyecto.id:
                self._proyectos.remove(p)
                return True
        return False

    @property
    def proyectos(self) -> tuple:
        return tuple(self._proyectos)

    @property
    @abstractmethod
    def tipo(self) -> str:
        """Texto que se guarda en la columna tipo_empleado."""

    @abstractmethod
    def obtener_permisos(self) -> list:
        """Cada rol resuelve sus permisos a su manera (polimorfismo)."""

    def mostrar_datos(self) -> str:
        return (f"ID: {self._id} | RUT: {self._rut} | Nombre: {self._nombre} "
                f"| Correo: {self._correo} | Salario Base: ${self._salario_base:,.2f}")


class EmpleadoRegular(Empleado):
    @property
    def tipo(self) -> str: return "REGULAR"

    def obtener_permisos(self) -> list:
        return ["ver_proyectos", "registrar_horas", "cambiar_contrasena"]

    def ver_proyectos(self) -> list:
        return [p.nombre for p in self._proyectos]

    def mostrar_datos(self) -> str:
        return f"[Regular] {super().mostrar_datos()}"


class Administrador(Empleado):
    @property
    def tipo(self) -> str: return "ADMINISTRADOR"

    def obtener_permisos(self) -> list:
        return ["ver_proyectos", "registrar_horas", "cambiar_contrasena",
                "gestionar_datos", "asignar_empleados", "desasignar_empleados",
                "generar_informes", "gestionar_usuarios"]

    def asignar_empleado_proyecto(self, empleado: Empleado, proyecto) -> bool:
        """Relaciona en memoria a ambos objetos. La persistencia la hace el DAO."""
        if not empleado.agregar_proyecto(proyecto):
            return False
        proyecto.agregar_empleado(empleado)
        return True

    def desasignar_empleado_de_proyecto(self, empleado: Empleado, proyecto) -> bool:
        if not empleado.quitar_proyecto(proyecto):
            return False
        proyecto.quitar_empleado(empleado)
        return True

    def mostrar_datos(self) -> str:
        return f"[Administrador] {super().mostrar_datos()}"
