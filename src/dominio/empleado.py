from dominio.registroTiempo import RegistroTiempo

class Empleado:
    def __init__(self, nombre: str, correo: str, id=None):
        self._id = id
        self._nombre = nombre
        self._correo = correo
        self._registros_tiempo: list[RegistroTiempo] = []

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
    def correo(self) -> str:
        return self._correo

    def agregar_registro_tiempo(self, registro: RegistroTiempo):
        self._registros_tiempo.append(registro)

    def mostrar_datos(self) -> str:
        return f"ID: {self._id} | Nombre: {self._nombre} | Correo: {self._correo}"


class EmpleadoRegular(Empleado):
    def __init__(self, nombre: str, correo: str, id=None):
        super().__init__(nombre, correo, id)


class Administrador(Empleado): 
    def __init__(self, nombre: str, correo: str, id=None):
        super().__init__(nombre, correo, id)


