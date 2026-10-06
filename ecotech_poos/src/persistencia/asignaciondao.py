from persistencia.base_dao import BaseDAO
from persistencia.conexion import Conexion
from persistencia.empleadodao import EmpleadoDAO
from persistencia.proyectodao import ProyectoDAO


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
    def proyectos_de_empleado(id_empleado: int) -> list:
        m = Conexion.marcador_sql()
        filas = AsignacionDAO.ejecutar_consulta(
            "SELECT p.id, p.nombre, p.presupuesto FROM proyecto p "
            "JOIN empleado_proyecto ep ON ep.id_proyecto = p.id "
            f"WHERE ep.id_empleado = {m} ORDER BY p.id", (id_empleado,))
        return [ProyectoDAO._fila_a_proyecto(f) for f in filas]

    @staticmethod
    def empleados_de_proyecto(id_proyecto: int) -> list:
        m = Conexion.marcador_sql()
        columnas = ", ".join(f"e.{c.strip()}" for c in
                                "id, rut, nombre, correo, departamento_id, tipo_empleado, salario_base".split(","))
        filas = AsignacionDAO.ejecutar_consulta(
            f"SELECT {columnas} FROM empleado e "
            "JOIN empleado_proyecto ep ON ep.id_empleado = e.id "
            f"WHERE ep.id_proyecto = {m} ORDER BY e.id", (id_proyecto,))
        return [EmpleadoDAO.fila_a_empleado(f) for f in filas]
