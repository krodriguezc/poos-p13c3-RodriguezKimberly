from dominio.registro_tiempo import RegistroTiempo
from persistencia.base_dao import BaseDAO
from persistencia.conexion import Conexion

COLUMNAS = "id, id_empleado, id_proyecto, horas, fecha, descripcion_tarea"


class RegistroTiempoDAO(BaseDAO):
    @staticmethod
    def fila_a_registro(fila) -> RegistroTiempo:
        return RegistroTiempo(id_empleado=fila[1], id_proyecto=fila[2], horas=float(fila[3]),
                            fecha=str(fila[4]), descripcion_tarea=fila[5], id=fila[0])

    @staticmethod
    def insertar(registro: RegistroTiempo) -> RegistroTiempo:
        m = Conexion.marcador_sql()
        _, nuevo_id = RegistroTiempoDAO.ejecutar_escritura(
            f"INSERT INTO registro_tiempo (id_empleado, id_proyecto, horas, fecha, descripcion_tarea) "
            f"VALUES ({m}, {m}, {m}, {m}, {m})",
            (registro.id_empleado, registro.id_proyecto, registro.horas, registro.fecha, registro.descripcion_tarea))
        registro.id = nuevo_id
        return registro

    @staticmethod
    def listar() -> list:
        filas = RegistroTiempoDAO.ejecutar_consulta(f"SELECT {COLUMNAS} FROM registro_tiempo ORDER BY id")
        return [RegistroTiempoDAO.fila_a_registro(f) for f in filas]

    @staticmethod
    def listar_por_empleado(id_empleado: int) -> list:
        m = Conexion.marcador_sql()
        filas = RegistroTiempoDAO.ejecutar_consulta(
            f"SELECT {COLUMNAS} FROM registro_tiempo WHERE id_empleado = {m} ORDER BY id", (id_empleado,))
        return [RegistroTiempoDAO.fila_a_registro(f) for f in filas]

    @staticmethod
    def listar_por_proyecto(id_proyecto: int) -> list:
        m = Conexion.marcador_sql()
        filas = RegistroTiempoDAO.ejecutar_consulta(
            f"SELECT {COLUMNAS} FROM registro_tiempo WHERE id_proyecto = {m} ORDER BY id", (id_proyecto,))
        return [RegistroTiempoDAO.fila_a_registro(f) for f in filas]

    @staticmethod
    def buscar_por_id(id_registro: int):
        m = Conexion.marcador_sql()
        fila = RegistroTiempoDAO.ejecutar_consulta(
            f"SELECT {COLUMNAS} FROM registro_tiempo WHERE id = {m}", (id_registro,), uno=True)
        return None if fila is None else RegistroTiempoDAO.fila_a_registro(fila)

    @staticmethod
    def actualizar(registro: RegistroTiempo) -> bool:
        m = Conexion.marcador_sql()
        filas, _ = RegistroTiempoDAO.ejecutar_escritura(
            f"UPDATE registro_tiempo SET horas = {m}, fecha = {m}, descripcion_tarea = {m} WHERE id = {m}",
            (registro.horas, registro.fecha, registro.descripcion_tarea, registro.id))
        return filas > 0

    @staticmethod
    def eliminar(id_registro: int) -> bool:
        m = Conexion.marcador_sql()
        filas, _ = RegistroTiempoDAO.ejecutar_escritura(
            f"DELETE FROM registro_tiempo WHERE id = {m}", (id_registro,))
        return filas > 0