from abc import ABC, abstractmethod

from dominio.registro_tiempo import RegistroTiempo
from dominio.validador_entrada import ValidadorEntrada as Val

#Clase base abstracta que guarda lo común a todo empleado.
class Empleado(ABC):
    def __init__(self, rut: str, nombre: str, correo: str = "", direccion: str = "", telefono: str = "",
                fecha_inicio_contrato: str = "", salario_base: float = 0.0,
                departamento_id: int = None, id: int = None):
        self._id = id
        self._rut = Val.validar_rut(rut)
        self._nombre = Val.validar_texto_no_vacio(nombre, "El nombre")
        self._correo = Val.validar_email_opcional(correo)
        self._direccion = Val.validar_texto_no_vacio(direccion, "La dirección")
        self._telefono = Val.validar_telefono(telefono)
        self._fecha_inicio_contrato = Val.validar_fecha(fecha_inicio_contrato)
        self._salario_base = Val.validar_monto(salario_base, "El salario")
        self._departamento_id = departamento_id          
        self._registros_tiempo: list[RegistroTiempo] = []
        self._proyectos: list = []                        # asociación Empleado 0..* — 0..* Proyecto

#Encapsulamiento con atributos privados con acceso controlado 
    @property
    def id(self): return self._id
    @id.setter
    def id(self, nuevo_id): self._id = nuevo_id

    @property
    def rut(self) -> str: return self._rut            

    @property
    def nombre(self) -> str: return self._nombre
    @nombre.setter
    def nombre(self, nuevo: str): self._nombre = Val.validar_texto_no_vacio(nuevo, "El nombre")

    @property
    def correo(self) -> str: return self._correo

    @property
    def direccion(self) -> str: return self._direccion

    @property
    def telefono(self) -> str: return self._telefono

    @property
    def fecha_inicio_contrato(self) -> str: return self._fecha_inicio_contrato

    @property
    def salario_base(self) -> float: return self._salario_base
    @salario_base.setter
    def salario_base(self, monto: float): self._salario_base = Val.validar_monto(monto, "El salario")

    @property
    def departamento_id(self): return self._departamento_id
    @departamento_id.setter
    def departamento_id(self, dep_id): self._departamento_id = dep_id

#Operaciones del UML
    def actualizar_datos(self, direccion: str, telefono: str, correo: str) -> None:
        direccion = Val.validar_texto_no_vacio(direccion, "La dirección")
        telefono = Val.validar_telefono(telefono)
        correo = Val.validar_email_opcional(correo)
        self._direccion, self._telefono, self._correo = direccion, telefono, correo

#Aqui se asocia registrotiempo con el empleado
    def registrar_horas(self, id_proyecto: int, horas: float, fecha: str, descripcion_tarea: str) -> RegistroTiempo:
        if self._id is None:
            raise ValueError("El empleado debe estar guardado antes de registrar horas.")
        registro = RegistroTiempo(self._id, id_proyecto, horas, fecha, descripcion_tarea)
        self._registros_tiempo.append(registro)
        return registro

    @abstractmethod
    def obtener_permisos(self) -> list:
        """cada rol resuelve sus permisos a su manera con polimorfismo."""

    def tiene_permiso(self, permiso: str) -> bool:
        return permiso in self.obtener_permisos()

    @property
    @abstractmethod
    def tipo(self) -> str:
        """Tipo de empleado regular o administrador."""
    def agregar_registro_tiempo(self, registro: RegistroTiempo) -> bool:
        if any(r.id is not None and r.id == registro.id for r in self._registros_tiempo):
            return False
        self._registros_tiempo.append(registro)
        return True

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

    def mostrar_datos(self) -> str:
        return (f"ID: {self._id} | RUT: {self._rut} | Nombre: {self._nombre} | Correo: {self._correo} "
                f"| Tel: {self._telefono} | Inicio contrato: {self._fecha_inicio_contrato} "
                f"| Salario Base: ${self._salario_base:,.2f}")

#Empleado con rol regular: consulta sus proyectos y registra sus horas.
class EmpleadoRegular(Empleado):
    @property
    def tipo(self) -> str: return "REGULAR"

    def obtener_permisos(self) -> list:
        return ["ver_proyectos", "registrar_horas", "cambiar_contrasena"]

    def ver_proyectos(self) -> list:
        return [p.nombre for p in self._proyectos]

    def mostrar_datos(self) -> str:
        return f"[Regular] {super().mostrar_datos()}"

#Empleado con permisos de gestión
class Administrador(Empleado):
    @property
    def tipo(self) -> str: return "ADMINISTRADOR"

    def obtener_permisos(self) -> list:
        return ["ver_proyectos", "registrar_horas", "cambiar_contrasena",
                "gestionar_datos", "asignar_empleados", "generar_informes", "gestionar_usuarios"]

    def asignar_empleado_proyecto(self, empleado: Empleado, proyecto) -> bool:
        if not empleado.agregar_proyecto(proyecto):
            return False
        proyecto.agregar_empleado(empleado)
        return True

    def desasignar_empleado_de_proyecto(self, empleado: Empleado, proyecto) -> bool:
        if not empleado.quitar_proyecto(proyecto):
            return False
        proyecto.remover_empleado(empleado)
        return True

    def mostrar_datos(self) -> str:
        return f"[Administrador] {super().mostrar_datos()}"
