from dominio.registroTiempo import RegistroTiempo
from persistencia.base_dao import BaseDAO
from persistencia.conexion import Conexion

_COLUMNAS = "id, id_empleado, id_proyecto, horas, fecha"


class RegistroTiempoDAO(BaseDAO):
    @staticmethod
    def _fila_a_registro(fila) -> RegistroTiempo:
        return RegistroTiempo(id_empleado=fila[1], id_proyecto=fila[2], horas=fila[3], fecha=fila[4], id=fila[0])

    @staticmethod
    def insertar(registro: RegistroTiempo) -> RegistroTiempo:
        m = Conexion.marcador_sql()
        _, nuevo_id = RegistroTiempoDAO.ejecutar_escritura(
            f"INSERT INTO registro_tiempo (id_empleado, id_proyecto, horas, fecha) VALUES ({m}, {m}, {m}, {m})",
            (registro.id_empleado, registro.id_proyecto, registro.horas, registro.fecha))
        registro.id = nuevo_id
        return registro

    @staticmethod
    def listar() -> list:
        filas = RegistroTiempoDAO.ejecutar_consulta(f"SELECT {_COLUMNAS} FROM registro_tiempo ORDER BY id")
        return [RegistroTiempoDAO._fila_a_registro(f) for f in filas]

    @staticmethod
    def buscar_por_id(id_registro: int):
        m = Conexion.marcador_sql()
        fila = RegistroTiempoDAO.ejecutar_consulta(
            f"SELECT {_COLUMNAS} FROM registro_tiempo WHERE id = {m}", (id_registro,), uno=True)
        return None if fila is None else RegistroTiempoDAO._fila_a_registro(fila)

    @staticmethod
    def actualizar(registro: RegistroTiempo) -> bool:
        m = Conexion.marcador_sql()
        filas, _ = RegistroTiempoDAO.ejecutar_escritura(
            f"UPDATE registro_tiempo SET horas = {m}, fecha = {m} WHERE id = {m}",
            (registro.horas, registro.fecha, registro.id))
        return filas > 0

    @staticmethod
    def eliminar(id_registro: int) -> bool:
        m = Conexion.marcador_sql()
        filas, _ = RegistroTiempoDAO.ejecutar_escritura(
            f"DELETE FROM registro_tiempo WHERE id = {m}", (id_registro,))
        return filas > 0
