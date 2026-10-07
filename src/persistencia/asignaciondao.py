from persistencia import empleadodao, proyectodao
from persistencia.base_dao import BaseDAO
from persistencia.conexion import Conexion

# empleado a proyecto 0..* - 0..*
class AsignacionDAO(BaseDAO):
    @staticmethod
    def asignar(id_empleado: int, id_proyecto: int) -> bool:
        m = Conexion.marcador_sql()
        filas, _ = AsignacionDAO.ejecutar_escritura(
            f"INSERT INTO empleado_proyecto (id_empleado, id_proyecto) VALUES ({m}, {m})",
            (id_empleado, id_proyecto))
        return filas > 0

    @staticmethod
    def desasignar(id_empleado: int, id_proyecto: int) -> bool:
        m = Conexion.marcador_sql()
        filas, _ = AsignacionDAO.ejecutar_escritura(
            f"DELETE FROM empleado_proyecto WHERE id_empleado = {m} AND id_proyecto = {m}",
            (id_empleado, id_proyecto))
        return filas > 0

    @staticmethod
    def existe(id_empleado: int, id_proyecto: int) -> bool:
        m = Conexion.marcador_sql()
        fila = AsignacionDAO.ejecutar_consulta(
            f"SELECT 1 FROM empleado_proyecto WHERE id_empleado = {m} AND id_proyecto = {m}",
            (id_empleado, id_proyecto), uno=True)
        return fila is not None

    @staticmethod
    def proyectos_de_empleado(id_empleado: int) -> list:
        m = Conexion.marcador_sql()
        filas = AsignacionDAO.ejecutar_consulta(
            f"SELECT {proyectodao.COLUMNAS} FROM proyecto WHERE id IN "
            f"(SELECT id_proyecto FROM empleado_proyecto WHERE id_empleado = {m}) ORDER BY id", (id_empleado,))
        return [proyectodao.ProyectoDAO.fila_a_proyecto(f) for f in filas]

    @staticmethod
    def empleados_de_proyecto(id_proyecto: int) -> list:
        m = Conexion.marcador_sql()
        filas = AsignacionDAO.ejecutar_consulta(
            f"SELECT {empleadodao.COLUMNAS} FROM empleado WHERE id IN "
            f"(SELECT id_empleado FROM empleado_proyecto WHERE id_proyecto = {m}) ORDER BY id", (id_proyecto,))
        return [empleadodao.EmpleadoDAO.fila_a_empleado(f) for f in filas]