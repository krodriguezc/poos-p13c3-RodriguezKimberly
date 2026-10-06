from dominio.validador_entrada import ValidadorEntrada


class RegistroTiempo:
    def __init__(self, id_empleado: int, id_proyecto: int, horas: float, fecha: str, id: int = None):
        self._id = id
        self._id_empleado = id_empleado
        self._id_proyecto = id_proyecto
        self._horas = ValidadorEntrada.validar_horas(horas)
        self._fecha = ValidadorEntrada.validar_fecha(fecha)

    @property
    def id(self): return self._id
    @id.setter
    def id(self, nuevo_id): self._id = nuevo_id

    @property
    def id_empleado(self): return self._id_empleado

    @property
    def id_proyecto(self): return self._id_proyecto

    @property
    def horas(self) -> float: return self._horas
    @horas.setter
    def horas(self, valor: float): self._horas = ValidadorEntrada.validar_horas(valor)

    @property
    def fecha(self) -> str: return self._fecha
    @fecha.setter
    def fecha(self, valor: str): self._fecha = ValidadorEntrada.validar_fecha(valor)

    def mostrar_datos(self) -> str:
        return (f"ID: {self._id} | Fecha: {self._fecha} | Empleado ID: {self._id_empleado} "
                f"| Proyecto ID: {self._id_proyecto} | Horas: {self._horas} hrs")
